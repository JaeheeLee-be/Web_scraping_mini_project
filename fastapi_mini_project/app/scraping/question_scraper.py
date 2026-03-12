import asyncio
import requests
from bs4 import BeautifulSoup
# 경로가 app.scraping에 있으므로, 상위 패키지의 repository를 가져옵니다.
from app.repositories import question_repo


async def run_question_scraper(max_pages: int = 5):
    base_url = "https://saramro.com"
    list_url = f"{base_url}/goodread"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    total_count = 0

    for page in range(1, max_pages + 1):
        try:
            resp = session.get(f"{list_url}?page={page}", headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            links = soup.select("div.bo_tit a")
            if not links:
                break

            page_data = []
            for link in links:
                detail_url = link.get('href')
                # 1단계: 상세 페이지 접속
                detail_resp = session.get(detail_url, headers=headers, timeout=10)
                detail_soup = BeautifulSoup(detail_resp.text, "html.parser")

                content_el = detail_soup.select_one("#bo_v_con")

                if content_el:
                    full_content = content_el.get_text(separator="\n", strip=True)
                    # 2단계: 문장 단위로 쪼개기 (옵션)
                    # 만약 01. 02. 처럼 되어 있는걸 각각 저장하고 싶다면 아래처럼 처리
                    lines = [line.strip() for line in full_content.split('\n') if line.strip()]

                    for line in lines:
                        # 숫자+점(01.)으로 시작하는 문장만 골라내거나 혹은 전체 저장
                        if line[0].isdigit():
                            page_data.append({"content": line})

                await asyncio.sleep(0.1)  # 상세 페이지 간 짧은 대기

            # 3단계: 페이지 단위 bulk 저장
            if page_data:
                await question_repo.bulk_create_questions(page_data)
                total_count += len(page_data)
                print(f"📦 {page}페이지 저장 완료 ({len(page_data)}건)")

        except Exception as e:
            print(f"❌ {page}페이지 작업 중 에러: {e}")
            break

    return f"✅ 총 {total_count}개의 질문 데이터를 저장했습니다."
import asyncio
import requests
from bs4 import BeautifulSoup
from app.repositories import question_repo


async def run_question_scraper(max_pages: int = 5):
    base_url = "https://saramro.com"
    list_url = f"{base_url}/goodread"
    headers = {
        "User-Agent": "python-requests/2.31.0"
    }

    session = requests.Session()  # 세션 연결 상태 유지
    total_count = 0  # 최종적으로 저장된 데이터 개수 확인

    for page in range(1, max_pages + 1):
        try:
            # 1. 목록 페이지 요청
            resp = session.get(f"{list_url}?page={page}", headers=headers, timeout=10)
            resp.raise_for_status()  # HTTP 상태가 200이 아니면 에러 발생

            # 2. 파싱 및 상세 페이지 링크 추출
            soup = BeautifulSoup(resp.text, "html.parser")
            links = soup.select("div.bo_tit a")

            if not links:
                break

            page_data = []
            for link in links:
                detail_url = link.get('href')

                # 3. 상세 페이지 접속 및 데이터 추출
                detail_resp = session.get(detail_url, headers=headers, timeout=10)
                detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
                content_el = detail_soup.select_one("#bo_v_con")

                if content_el:
                    full_content = content_el.get_text(separator="\n", strip=True)
                    # 문장 단위 분리 및 정제
                    lines = [line.strip() for line in full_content.split('\n') if line.strip()]

                    for line in lines:
                        # 숫자와 점으로 시작하는 문장(예: 01.) 위주로 필터링하여 저장
                        if line and line[0].isdigit():
                            page_data.append({"content": line})

                await asyncio.sleep(0.1)  # 상세 페이지 간 짧은 대기

            # 4. DB 저장 및 카운트
            if page_data:
                await question_repo.bulk_create_questions(page_data)  # 비동기로 한번에 저장
                total_count += len(page_data)
            else:
                break

            await asyncio.sleep(0.5)  # 서버 부하 방지 및 차단 방지

        except Exception as e:
            return f"에러 발생 ({page}p): {str(e)}"

    return f"총 {total_count}개의 질문 데이터를 저장"
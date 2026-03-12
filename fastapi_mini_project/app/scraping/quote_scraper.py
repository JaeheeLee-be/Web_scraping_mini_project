import asyncio
import requests
from bs4 import BeautifulSoup
from app.repositories import quote_repo


async def run_quote_scraper(max_pages: int = 5):
    base_url = "https://saramro.com"
    list_url = f"{base_url}/quotes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    total_count = 0

    for page in range(1, max_pages + 1):
        try:
            # 1. 목록 페이지 요청
            resp = session.get(f"{list_url}?page={page}", headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            # 목록에서 상세 페이지로 가는 링크들 추출
            links = soup.select("div.bo_tit a")

            if not links:
                break  # 더 이상 명언이 없으면 중단

            page_data = []
            for link in links:
                detail_url = link.get('href')
                # 혹시 상대 경로일 경우를 대비해 절대 경로로 보정 (필요시)
                if not detail_url.startswith("http"):
                    detail_url = base_url + detail_url

                try:
                    # 2. 상세 페이지 접속 (내용을 더 정확하게 가져오기 위함)
                    detail_resp = session.get(detail_url, headers=headers, timeout=10)
                    detail_soup = BeautifulSoup(detail_resp.text, "html.parser")

                    # 상세 페이지의 본문 요소 (#bo_v_con)
                    content_el = detail_soup.select_one("#bo_v_con")

                    if content_el:
                        # 텍스트 추출 및 정제
                        raw_content = content_el.get_text(strip=True)

                        # 저자 분리 로직 (내용 - 저자 형태 대응)
                        if " - " in raw_content:
                            parts = raw_content.rsplit(" - ", 1)
                            content = parts[0].strip()
                            author = parts[1].strip()
                        elif "-" in raw_content:
                            parts = raw_content.rsplit("-", 1)
                            content = parts[0].strip()
                            author = parts[1].strip()
                        else:
                            content = raw_content
                            author = "작자 미상"

                        page_data.append({"content": content, "author": author})
                        total_count += 1

                    # 서버 부하 방지를 위해 아주 짧게 대기
                    await asyncio.sleep(0.2)

                except Exception as e:
                    print(f"⚠️ 상세 페이지 에러 ({detail_url}): {e}")
                    continue

            # 3. 한 페이지 분량의 데이터를 모아서 DB 저장
            if page_data:
                await quote_repo.bulk_create_quotes(page_data)

            print(f" {page}페이지 수집 완료 ({len(page_data)}개)")

        except Exception as e:
            return f" 에러 발생 ({page}p): {str(e)}"

    return f"총 {total_count}개의 명언을 저장"
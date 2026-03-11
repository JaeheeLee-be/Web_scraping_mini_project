import asyncio
import requests
from bs4 import BeautifulSoup
from app.repositories import quote_repo


async def run_quote_scraper(max_pages: int = 5):
    url = "https://saramro.com/quotes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://saramro.com/"
    }

    session = requests.Session()
    total_count = 0

    for page in range(1, max_pages + 1):
        try:
            # 1. 페이지 요청
            resp = session.get(f"{url}?page={page}", headers=headers, timeout=10)
            resp.raise_for_status()

            # 2. 파싱 및 데이터 추출
            soup = BeautifulSoup(resp.text, "html.parser")
            rows = soup.select("table.tbl_head01 tbody tr")

            page_data = []
            for i in range(0, len(rows) - 1, 2):
                title_el = rows[i].select_one("div.bo_tit a")
                content_el = rows[i + 1].select_one("td")

                if title_el and content_el:
                    # 저자명 분리 및 본문 정제
                    title_text = title_el.get_text(strip=True)
                    author = title_text.rsplit("-", 1)[-1].strip() if "-" in title_text else "작자 미상"
                    content = content_el.get_text(separator="\n", strip=True).split("-")[0].strip()

                    page_data.append({"content": content, "author": author})

            # 3. DB 저장 및 카운트
            if page_data:
                await quote_repo.bulk_create_quotes(page_data)
                total_count += len(page_data)
            else:
                break  # 더 이상 데이터가 없으면 중단

            await asyncio.sleep(0.5)  # 차단 방지

        except Exception as e:
            return f"에러 발생 ({page}p): {str(e)}"

    return f"성공! 총 {total_count}개의 명언을 저장했습니다."
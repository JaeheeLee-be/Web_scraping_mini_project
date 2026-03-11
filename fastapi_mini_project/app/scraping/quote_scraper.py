import requests
from bs4 import BeautifulSoup
from app.repositories import quote_repo


async def run_quote_scraper():
    url = "https://saramro.com/quotes"

    # 테스트에서 성공했던 상세 헤더 적용
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://saramro.com/"
    }

    try:
        # 세션을 사용하여 연결 안정성 확보
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # 테스트에서 성공한 방식대로 테이블 찾기
        table = soup.select_one("table.tbl_head01") or soup.find("table")
        if not table:
            return "테이블 구조를 찾을 수 없습니다."

        tbody = table.find("tbody")
        if not tbody:
            return "tbody 구조를 찾을 수 없습니다."

        # 모든 행(tr)을 가져옵니다.
        rows = tbody.find_all("tr", recursive=False)

        scraped_data = []
        # 2개 행(제목+본문)을 한 세트로 처리
        for i in range(0, len(rows) - 1, 2):
            title_row = rows[i]
            content_row = rows[i + 1]

            # 1. 제목행에서 저자 추출
            link_el = title_row.select_one("div.bo_tit a")
            author = "작자 미상"
            if link_el:
                title_text = link_el.get_text(strip=True)
                if "-" in title_text:
                    author = title_text.rsplit("-", 1)[-1].strip()

            # 2. 본문행에서 실제 명언 내용 추출
            content_el = content_row.select_one("td")
            if content_el:
                content = content_el.get_text(separator="\n", strip=True)
                # 본문 하단에 저자가 또 붙어있는 경우 잘라내기
                content = content.split("-")[0].strip()

                scraped_data.append({
                    "content": content,
                    "author": author
                })

        if scraped_data:
            # 레포지토리를 통해 DB 저장
            await quote_repo.bulk_create_quotes(scraped_data)
            return f"성공! {len(scraped_data)}개의 명언을 저장했습니다."

        return "데이터를 찾지 못했습니다."

    except Exception as e:
        return f"스크래핑 중 에러 발생: {str(e)}"
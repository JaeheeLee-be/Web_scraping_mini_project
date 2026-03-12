import asyncio
import requests
from bs4 import BeautifulSoup
from app.repositories import quote_repo


async def run_quote_scraper(max_pages: int = 5):
    url = "https://saramro.com/quotes"
    headers = {
        "User-Agent": "python-requests/2.31.0"
    }

    session = requests.Session()      # 세션 연결 상태 유지
    total_count = 0                   # 최종적으로 저장된 데이터 개수 확인

    for page in range(1, max_pages + 1):
        try:
            # 1. 페이지 요청
            resp = session.get(f"{url}?page={page}", headers=headers, timeout=10)
            resp.raise_for_status() # HTTP 상태가 200이 아니면 에러 발생한것

            # 2. 파싱 및 데이터 추출
            soup = BeautifulSoup(resp.text, "html.parser") # HTML 텍스트를 파이썬 객체로 변환
            rows = soup.select("table.tbl_head01 tbody tr") # 특정 테이블의 행만 추출

            page_data = []
            for i in range(0, len(rows) - 1, 2):       # 2줄이 한 세트인 경우 2칸씩 뛰어 씀
                title_el = rows[i].select_one("div.bo_tit a") # 제목 요소 선택
                content_el = rows[i + 1].select_one("td")     # 내용 요소 선택

                if title_el and content_el:
                    # 저자명 분리 및 본문 정제
                    title_text = title_el.get_text(strip=True) #앞 뒤 공백 제거
                    author = title_text.rsplit("-", 1)[-1].strip() if "-" in title_text else "작자 미상"  # 하이픈 기준으로 저자 추출
                    content = content_el.get_text(separator="\n", strip=True).split("-")[0].strip()     # 본문 텍스트 추출

                    page_data.append({"content": content, "author": author})  #딕셔너리 형태로 저장

            # 3. DB 저장 및 카운트
            if page_data:
                await quote_repo.bulk_create_quotes(page_data)   # 비동기로 한번에 저장
                total_count += len(page_data)
            else:
                break  # 더 이상 데이터가 없으면 중단

            await asyncio.sleep(0.5)  # 서버 부하 방지 및 차단 방지

        except Exception as e:
            return f"에러 발생 ({page}p): {str(e)}"

    return f"총 {total_count}개의 명언을 저장"
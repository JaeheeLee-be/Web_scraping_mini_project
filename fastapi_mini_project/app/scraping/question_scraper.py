import asyncio
import requests
from bs4 import BeautifulSoup
from app.repositories import question_repo


async def run_question_scraper(max_pages: int = 5):
    base_url = "https://saramro.com"
    # URL 구조를 명확히 합니다.
    list_url = f"{base_url}/goodread"

    # 1. User-Agent를 실제 브라우저처럼 보이게 수정 (차단 방지 핵심)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    timeout_config = 15  # 타임아웃 약간 늘림

    session = requests.Session()
    total_count = 0

    for page in range(1, max_pages + 1):
        try:
            # 2. 목록 페이지 요청
            # params를 사용하여 쿼리 스트링을 안전하게 전달
            resp = session.get(list_url, headers=headers, params={"page": page}, timeout=timeout_config)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            # 게시판 목록의 링크 추출 (경로가 상대경로인지 절대경로인지 체크)
            links = soup.select("div.bo_tit a")

            if not links:
                print(f"{page}페이지에 링크가 없습니다.")
                break

            page_data = []
            for link in links:
                detail_url = link.get('href')
                # 만약 detail_url이 상대경로(/goodread/123)라면 base_url을 붙여줘야 함
                if detail_url.startswith('/'):
                    detail_url = base_url + detail_url

                try:
                    # 3. 상세 페이지 접속
                    detail_resp = session.get(detail_url, headers=headers, timeout=timeout_config)
                    detail_soup = BeautifulSoup(detail_resp.text, "html.parser")
                    content_el = detail_soup.select_one("#bo_v_con")

                    if content_el:
                        full_content = content_el.get_text(separator="\n", strip=True)
                        lines = [line.strip() for line in full_content.split('\n') if line.strip()]

                        for line in lines:
                            # '01. 질문' 형태만 필터링
                            if line and line[0].isdigit():
                                page_data.append({"content": line})

                    # 상세 페이지 사이의 딜레이
                    await asyncio.sleep(0.2)

                except Exception as detail_e:
                    print(f"상세 페이지({detail_url}) 스킵: {detail_e}")
                    continue

            # 4. DB 저장
            if page_data:
                await question_repo.bulk_create_questions(page_data)
                total_count += len(page_data)
                print(f"{page}페이지 저장 완료: {len(page_data)}개 추출됨")
            else:
                print(f"{page}p 추출된 문장이 없습니다.")

            await asyncio.sleep(1.0)  # 페이지 간 충분한 휴식

        except Exception as e:
            print(f"에러 발생 ({page}p): {str(e)}")
            # 한 페이지 에러나도 다음 페이지 시도하려면 return 대신 continue
            continue

    return f"총 {total_count}개의 질문 데이터를 저장"
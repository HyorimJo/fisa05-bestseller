from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import datetime
import time

def fetch_kyobo_best_sellers():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 교보문고 베스트셀러 페이지 접속
        page.goto("https://www.kyobobook.co.kr/bestseller/online", timeout=60000)

        # JavaScript 렌더링 시간 확보
        time.sleep(5)

        # 렌더링 완료된 HTML 가져오기
        html = page.content()
        browser.close()

        soup = BeautifulSoup(html, "html.parser")

        # 책 정보 추출
        books = []
        for idx, item in enumerate(soup.select("div.detail"), start=1):
            title_tag = item.select_one("div.title")
            author_tag = item.select_one("div.author")

            if title_tag and author_tag:
                title = title_tag.text.strip()
                author = author_tag.text.strip().replace('\n', '').replace('저자 더보기', '')
                books.append(f"{idx}. **{title}** - _{author}_")

            if idx >= 20:  # 상위 20권만 수집
                break

        return books

def update_readme(books):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = f"# 📚 교보문고 베스트셀러 (업데이트: {now})\n\n"

    if books:
        content += "\n".join(books)
    else:
        content += "❗️베스트셀러 정보를 불러오지 못했습니다."

    content += "\n\n자동 업데이트: GitHub Actions 사용"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    books = fetch_kyobo_best_sellers()
    update_readme(books)

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_aladin_bestsellers():
    url = "https://www.aladin.co.kr/shop/wbrowse.aspx?CID=8256"  # 종합 베스트
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for idx, item in enumerate(soup.select("div.ss_book_box")[:20], start=1):
        title_tag = item.select_one("a.bo3")
        author_tag = item.select_one("div.ss_book_list > ul > li:nth-child(1)")
        if title_tag:
            title = title_tag.text.strip()
            author = author_tag.text.strip() if author_tag else "저자 정보 없음"
            books.append(f"{idx}. **{title}** - _{author}_")

    return books

def update_readme(books):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = f"# 📚 알라딘 베스트셀러 (업데이트: {now})\n\n"

    if books:
        content += "\n".join(books)
    else:
        content += "❗️베스트셀러 정보를 불러오지 못했습니다."

    content += "\n\n자동 업데이트: GitHub Actions 사용"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    best_sellers = fetch_aladin_bestsellers()
    update_readme(best_sellers)

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_kyobo_best_sellers():
    url = "https://www.kyobobook.co.kr/bestseller/online"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for idx, item in enumerate(soup.select("div.detail"), start=1):
        title_tag = item.select_one("div.title")
        author_tag = item.select_one("div.author")

        if title_tag and author_tag:
            title = title_tag.text.strip()
            author = author_tag.text.strip().replace('\n', '').replace('저자 더보기', '')
            books.append(f"{idx}. **{title}** - _{author}_")

        if idx >= 20:  # 상위 20권만 출력
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
    best_sellers = fetch_kyobo_best_sellers()
    update_readme(best_sellers)

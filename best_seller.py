# best_seller.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_yes24_best_sellers():
    url = "https://www.yes24.com/24/Category/BestSeller"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.encoding = 'euc-kr'
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for idx, item in enumerate(soup.select(".yesList .gd_info"), start=1):
        title = item.select_one("a.gd_name").text.strip()
        author = item.select_one("span.gd_auth").text.strip()
        books.append(f"{idx}. **{title}** - _{author}_")

    return books

def update_readme(books):
    today = datetime.now().strftime("%Y-%m-%d")
    content = f"# 📚 YES24 베스트셀러 ({today})\n\n"
    content += "\n".join(books)
    content += "\n\n자동 업데이트: GitHub Actions 사용"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    best_sellers = fetch_yes24_best_sellers()
    update_readme(best_sellers)

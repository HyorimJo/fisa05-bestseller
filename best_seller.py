import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_aladin_rss_bestsellers():
    url = "https://www.aladin.co.kr/rsscenter/rss_feeds.aspx?cid=0&type=Bestseller"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")

    books = []
    for idx, item in enumerate(soup.find_all("item")[:20], start=1):
        title = item.title.text.strip()
        link = item.link.text.strip()
        books.append(f"{idx}. [{title}]({link})")

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
    books = fetch_aladin_rss_bestsellers()
    update_readme(books)

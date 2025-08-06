from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from datetime import datetime

def fetch_kyobo_best_sellers():
    url = "http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf"
    html = urlopen(url)
    bsObject = bs(html, "html.parser")

    # 집계 기준 날짜 추출
    try:
        week_standard = bsObject.find('h4', {'class': 'title_best_basic'}).find('small').text.strip()
    except AttributeError:
        week_standard = "(날짜 정보를 불러올 수 없습니다)"

    # 베스트셀러 리스트 추출
    bestseller_contents = bsObject.find('ul', {'class': 'list_type01'})
    bestseller_list = bestseller_contents.findAll('div', {'class': 'detail'})

    books = []
    for idx, book in enumerate(bestseller_list[:20], start=1):
        title = book.find('div', {'class': 'title'}).find('strong').text.strip()
        subtitle = book.find('div', {'class': 'subtitle'}).text.strip()
        books.append(f"{idx}. **{title}**\n   - {subtitle}")

    return week_standard, books

def update_readme(week_standard, books):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    content = f"# 📚 교보문고 베스트셀러 (업데이트: {now})\n\n"
    content += f"📅 기준일: {week_standard}\n\n"

    if books:
        content += "\n".join(books)
    else:
        content += "❗️베스트셀러 정보를 불러오지 못했습니다."

    content += "\n\n자동 업데이트: GitHub Actions 사용"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    week_standard, best_sellers = fetch_kyobo_best_sellers()
    update_readme(week_standard, best_sellers)

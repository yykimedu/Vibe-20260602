import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://search.naver.com/search.naver"
QUERY = "반도체"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_search_html(query):
    params = {
        "where": "nexearch",
        "sm": "top_hty",
        "fbm": "0",
        "ie": "utf8",
        "query": query,
        "ackey": "rjs7cpaa",
    }
    response = requests.get(SEARCH_URL, params=params, headers=headers)
    response.raise_for_status()
    return response.text

def parse_news_results(html):
    soup = BeautifulSoup(html, "html.parser")
    news_items = []

    for a in soup.select("a.news_tit"):
        title = a.get_text(strip=True)
        link = a.get("href")
        summary = ""
        parent = a.find_parent("div", class_="news_area")
        if parent:
            summary_tag = parent.select_one("a.api_txt_lines.dsc_txt_wrap")
            if summary_tag:
                summary = summary_tag.get_text(strip=True)

        news_items.append({
            "title": title,
            "link": link,
            "summary": summary,
        })

    return news_items

def extract_article_text(article_url):
    response = requests.get(article_url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    selectors = [
        "article p",
        "div#newsEndContents p",
        "div.article_body p",
        "div#content p",
        "div._article_body_contents p",
    ]

    paragraphs = []
    for sel in selectors:
        found = soup.select(sel)
        if found:
            paragraphs = found
            break

    if not paragraphs:
        paragraphs = soup.find_all("p")

    text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
    return text

def main():
    html = get_search_html(QUERY)
    news_list = parse_news_results(html)

    for idx, news in enumerate(news_list[:5], start=1):
        print(f"=== 기사 {idx} ===")
        print("제목:", news["title"])
        print("링크:", news["link"])
        print("요약:", news["summary"])
        print()

        # 실제 기사 본문을 크롤링하려면 아래 주석을 해제하세요.
        # 본문 구조가 사이트마다 달라서 site-specific 파싱이 필요합니다.
        # article_text = extract_article_text(news["link"])
        # print(article_text[:1000])
        # print()

if __name__ == "__main__":
    main()
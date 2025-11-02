import scrapy
from bs4 import BeautifulSoup

class NewsSpider(scrapy.Spider):
    name = "news_spider"
    start_urls = [
        "https://www.bbc.com/news",
        "https://www.reuters.com/world/"
    ]
    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        if "bbc.com" in response.url:
            articles = soup.select('a.gs-c-promo-heading')
            for a in articles:
                title = a.get_text(strip=True)
                link = a.get("href")
                if link and link.startswith("/"):
                    link = "https://www.bbc.com" + link
                yield scrapy.Request(link, callback=self.parse_article, meta={"title": title, "source": "BBC"})
        if "reuters.com" in response.url:
            articles = soup.select("a[data-testid='Heading']")
            for a in articles:
                title = a.get_text(strip=True)
                link = a.get("href")
                if link and link.startswith("/"):
                    link = "https://www.reuters.com" + link
                yield scrapy.Request(link, callback=self.parse_article, meta={"title": title, "source": "Reuters"})
    def parse_article(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        full_text = " ".join(p.get_text(strip=True) for p in paragraphs)
        yield {
            "title": response.meta["title"],
            "source": response.meta["source"],
            "url": response.url,
            "text": full_text
        }

from datetime import datetime, timedelta
from typing import List,Dict

from bs4 import Tag,BeautifulSoup
from base.scraper import Scraper
from base.utils import get_html_from_url,get_element_text

"""start_date = datetime(2020,1,10)
end_date = datetime(2023, 1, 11)

current_date = start_date
date_format = "%Y%m%d"

while current_date <= end_date:
    cd = current_date.strftime(date_format)
    print(f"{current_date.year}/{cd}.html")
    current_date += timedelta(days=1)"""


class OrigoScraper(Scraper):
    def __init__(self):
        Scraper.__init__(self, base_url="https://origo.hu", portal_name="origo",portal_id=2)
        self.detail_soup = None

    def scrape_page(self,datestring:str):
        url = f"{self.base_url}/hir-archivum/{datestring[:4]}/{datestring}.html"

        soup = get_html_from_url(url)

        item_elements = soup.find_all("div",class_="archive-cikk")
        articles = self.scape_articles_from_page(item_elements)

        return articles

    def scape_articles_from_page(self, item_elements: List[Tag]) -> List[Dict]:
        articles = []
        for i in item_elements:
            articles.append(self.scrape_single_article(i))
        return articles

    """<div class="archive-cikk">
    <span>kedd 17:33</span>
    <h3><a href="https://www.origo.hu/gazdasag/20230110-gazdasag-penz-nmhh-internet-reklam-figyelmeztetes.html" title="Legyen nagyon óvatos, ha ilyen típusú reklámokkal találkozik az interneten">Legyen nagyon óvatos, ha ilyen típusú reklámokkal találkozik az interneten</a></h3>
    </div>
    """
    def scrape_yesterdays_articles(self):
        pass

    def scrape_title(self,soup):
        title = ""
        title_element = soup.select_one('a')
        if title_element:
            title = title_element['title']
        print("title: ",type(soup))
        return title

    def scrape_lead(self,soup):
        html = self.detail_soup()
        print(type(html))
        return get_element_text(html, '.article-lead > p')

    def scrape_author(self,soup):
        html = self.detail_soup()
        return get_element_text(html, 'span.article-author')

    def scrape_detail_url(self,soup):
        url = ""
        title_element = soup.select_one('a')
        if title_element:
            url = title_element['href']
        s = get_html_from_url(url)
        print("url: ",url)
        self.detail_soup = BeautifulSoup(str(s), 'html.parser')
        return url

    def scrape_full_text(self,soup):
        return ""

    def scrape_date(self,soup):
        html = self.detail_soup()
        div = html.select_one("div.article-date")
        if div["datetime"]:
            date_string = div["datetime"]
            date_format = "%Y-%m-%dT%H:%M"
            return datetime.strptime(date_string, date_format)
        url = self.scrape_detail_url(soup).split("/")
        return datetime.strptime(url[4][:8], '%Y%m%d')

    def scrape_category(self,soup):
        html = self.detail_soup()
        return get_element_text(html, 'span.opt-title')

    def scrape_image(self,soup):
        return ""
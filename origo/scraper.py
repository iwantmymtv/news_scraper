from datetime import datetime, timedelta
from typing import List,Dict

from bs4 import Tag,BeautifulSoup
from base.scraper import Scraper
from base.utils import get_html_from_url,get_element_text,get_element_from_result_set

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
        self.current_date_string = None

    def scrape_page(self,datestring:str) -> List[Dict]:
        self.current_date_string = datestring
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

    def scrape_title(self,soup:Tag) -> str:
        title = ""
        title_element = soup.select_one('a')
        if title_element:
            title = title_element['title']
        return title

    def scrape_lead(self,soup:Tag) -> str:
        html = self.detail_soup()
        print(type(html))
        return get_element_from_result_set(html, '.article-lead > p')

    def scrape_author(self,soup:Tag) -> str:
        html = self.detail_soup()
        return get_element_from_result_set(html, 'span.article-author')

    def scrape_detail_url(self,soup:Tag) -> str:
        url = ""
        title_element = soup.select_one('a')
        if title_element:
            url = title_element['href']
        s = get_html_from_url(url)

        self.detail_soup = BeautifulSoup(str(s), 'html.parser')
        return url

    def scrape_full_text(self,soup:Tag) -> str:
        # Parse the HTML of the web page
        html = self.detail_soup
        htmls = html.select(".article-content")
        string = ""
        for h in htmls:
            string += h.get_text()
        
        return string.strip().replace("\n","")

    def scrape_date(self,soup:Tag) -> datetime:
        html = self.detail_soup()
        div = get_element_from_result_set(html,"div.article-date")
        if div:
            #2023.01.10. 09:57
            date_format = "%Y.%m.%d. %H:%M"
            return datetime.strptime(div, date_format)

        return datetime.strptime(self.current_date_string, '%Y%m%d') 
        

    def scrape_category(self,soup:Tag) -> str:
        html = self.detail_soup()
        return get_element_from_result_set(html, 'span.opt-title')

    def scrape_image(self,soup:Tag) -> str:
        return ""
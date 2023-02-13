from datetime import datetime
from typing import List
from bs4 import Tag

from base.scraper import Scraper
from base.utils import get_element_text, get_html_from_url
from db.django import upload_many

from .config import conf


class HU24Scraper(Scraper):
    def __init__(self):
        Scraper.__init__(self, 
                         base_url=conf["BASE_URL"], 
                         portal_name=conf["PORTAL_NAME"],
                         portal_id=conf["PORTAL_ID"]
                         )
        self.categories = [
            "belfold",
            "kulfold",
            "gazdasag",
            "kultura",
            "tech",
            "elet-stilus",
            "szorakozas",
            "kozelet",
            "europoli",
            "uzleti-tippek",
            "tudomany",
            "sport",
            "otthon",
            "velemeny"
        ]
        self.default_date = datetime.now()

    def scrape_page(self, 
                    page: int = 1,
                    date=datetime.now().date(),
                    category:str = 'belfold',
                    save_to_bd:bool = False) -> List[dict]:

        self.default_date = date
        url = f"{self.base_url}/{category}/{date.year}/{date.month}/{date.day}/page/{page}/"

        soup = get_html_from_url(url)

        # Find all the elements with the class `list__item` and `article`
        item_elements = soup.find_all('div', {"class": ["m-articleWidget__innerWrap"]})

        articles = self.scape_articles_from_page(item_elements)
        print("articles:", articles)
        #save
        if save_to_bd:
            upload_many(articles)

        return articles

    def scape_articles_from_page(self, item_elements: List[Tag]) -> List[dict]:
        articles = []
        for i in item_elements:
            article = self.scrape_single_article(i)
            if self.base_url in article["url"]:
                articles.append(article)
        return articles

    def scrape_yesterdays_articles(self):
        pass

    def scrape_title(self,soup:Tag):
       return get_element_text(soup, 'a.m-articleWidget__link')
       
    def scrape_lead(self,soup:Tag):
        return get_element_text(soup, 'div.m-articleWidget__lead')

    def scrape_author(self,soup:Tag):
        return get_element_text(soup, 'a.m-author__name')

    def scrape_detail_url(self,soup:Tag):
        url = ""
        title_element = soup.select_one('a.m-articleWidget__link')
        if title_element:
            url = title_element['href']
        return url

    def scrape_full_text(self,soup:Tag):
        # Parse the HTML of the web page
        if not self.base_url in self.scrape_detail_url(soup):
            return ""
        html = get_html_from_url(self.scrape_detail_url(soup))
        htmls = html.select(".o-post__body.o-postCnt.post-body p")
        string = ""
        for h in htmls:
            string += h.get_text()
        #print(string.strip())
        return string.strip()
        

    def scrape_date(self,soup:Tag):
        #2023. 02. 10. 17:26
        date_format_hu = "%Y. %m. %d. %H:%M"
        date_string = get_element_text(soup, 'span.a-date').lower()
        try:
            date = datetime.strptime(date_string, date_format_hu)
        except:
            date = self.default_date
        return date

    def scrape_category(self,soup:Tag):
        return get_element_text(soup, 'a.m-articleWidget__tag')

    def scrape_image(self,soup:Tag):
        element = soup.select_one("a.m-articleWidget__linkImgWrap img")
        if element:
            return element.get('src').strip()
        else:
            return ""
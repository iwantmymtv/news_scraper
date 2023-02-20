from datetime import date
from bs4 import Tag
from base.scraper import Scraper
from index.utils import get_json_by_date
from .config import conf

class IndexScraper(Scraper):
    def __init__(self):
        Scraper.__init__(self, 
                         base_url=conf["BASE_URL"], 
                         portal_name=conf["PORTAL_NAME"],
                         portal_id=conf["PORTAL_ID"]
                         )
        self.current_page = None

    def scrape_yesterdays_articles(self):
        pass
    
    def scrape_page(self) -> None:
        articles = get_json_by_date(date=date.today())
        self.current_page = articles["list"]

    def scrape_articles_from_page(self):
        page = 1
        while True:
            self.scrape_page(1)
            if self.current_page:
                page += 1
                for i in self.current_page:
                    pass
            else:
                return

    def scrape_title(self,soup:Tag):
        pass

    def scrape_lead(self,soup:Tag):
        pass

    def scrape_author(self,soup:Tag):
        pass

    def scrape_detail_url(self,soup:Tag):
        pass

    def scrape_full_text(self,soup:Tag):
        pass

    def scrape_date(self,soup:Tag):
        pass

    def scrape_category(self,soup:Tag):
        pass

    def scrape_image(self,soup:Tag):
        pass
from bs4 import Tag

from base.scraper import Scraper

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

    def scrape_yesterdays_articles(self):
        pass

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
from abc import ABC, abstractmethod
from bs4 import ResultSet,Tag

from .utils import serialize_datetime

class Scraper(ABC):

    def __init__(self, base_url: str,portal_name: str,portal_id:int):
        self.base_url = base_url
        self.portal_name = portal_name
        self.portal_id = portal_id

    @abstractmethod
    def scrape_yesterdays_articles(self):
        pass

    @abstractmethod
    def scrape_title(self,soup:Tag):
        pass

    @abstractmethod
    def scrape_lead(self,soup:Tag):
        pass

    @abstractmethod
    def scrape_author(self,soup:Tag):
        pass

    @abstractmethod
    def scrape_detail_url(self,soup:Tag):
        pass

    @abstractmethod
    def scrape_full_text(self,soup:Tag):
        pass

    @abstractmethod
    def scrape_date(self,soup:Tag):
        pass

    @abstractmethod
    def scrape_category(self,soup:Tag):
        pass

    @abstractmethod
    def scrape_image(self,soup:Tag):
        pass
    
    def scrape_single_article(self,soup:Tag):
        url = self.scrape_detail_url(soup)
        article = {
            "portal":self.portal_id,
            "title":self.scrape_title(soup),
            "lead":self.scrape_lead(soup),
            "image":self.scrape_image(soup),
            "author": self.scrape_author(soup),
            "url":url,
            "category": self.scrape_category(soup),
            "full_text": self.scrape_full_text(soup),
            "date":serialize_datetime(self.scrape_date(soup))
        }

        return article



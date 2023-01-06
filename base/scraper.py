from abc import ABC, abstractmethod
from .utils import get_sentiment_analysis

class Scraper(ABC):

    def __init__(self, base_url: str,portal_name: str):
        self.base_url = base_url
        self.portal_name = portal_name

    @abstractmethod
    def scrape_yesterdays_articles(self):
        pass

    @abstractmethod
    def scrape_title(self,soup):
        pass

    @abstractmethod
    def scrape_lead(self,soup):
        pass

    @abstractmethod
    def scrape_author(self,soup):
        pass

    @abstractmethod
    def scrape_detail_url(self,soup):
        pass

    @abstractmethod
    def scrape_full_text(self,soup):
        pass

    @abstractmethod
    def scrape_date(self,soup):
        pass

    @abstractmethod
    def scrape_category(self,soup):
        pass
    
    def scrape_single_article(self,soup):
        title = self.scrape_title(soup)
        article = {
            "portal":self.portal_name,
            "title":title,
            "lead":self.scrape_lead(soup),
            "sentiment": get_sentiment_analysis(title),
            "author": self.scrape_author(soup),
            "url":self.scrape_detail_url(soup),
            "category": self.scrape_category(soup),
            "full_text": self.scrape_full_text(soup),
            "date":self.scrape_date(soup)
        }

        return article



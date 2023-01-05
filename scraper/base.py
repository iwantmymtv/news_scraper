from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
import requests

class Scraper(ABC):

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.db = None
        self.collection = None

    @abstractmethod
    def scrape_yesterdays_articles(self):
        pass

    def get_html_from_url(self, url: str) -> str:
        # Send an HTTP request to the website and save the response
        response = requests.get(url)

        # Parse the HTML of the web page
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup


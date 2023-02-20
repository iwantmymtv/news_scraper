from datetime import date
from bs4 import Tag
import requests
from base.scraper import Scraper

from .config import conf

class IndexScraper(Scraper):
    def __init__(self):
        Scraper.__init__(self, 
                         base_url=conf["BASE_URL"], 
                         portal_name=conf["PORTAL_NAME"],
                         portal_id=conf["PORTAL_ID"]
                         )
        self.current_page = None

    def get_json_by_date(self,date:date,page:int=1):
        date_string = f"{date.year}-{date.month}-{date.day}"
        url = "https://index.hu/api/json/"
        headers = {
            "Host": "index.hu",
            "Origin": "https://index.hu",
            "Referer": f"https://index.hu/24ora/?tol={date_string}&ig={date_string}",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26",
            }

        payload = {
            "rovat":"24ora",
            "url_params[pepe]": 1,
            "url_params[tol]": date_string,
            "url_params[ig]": date_string,
            "url_params[p]": page,
        }

        response = requests.get(url, params=payload,headers=headers)
        return response.json()
    
    def scrape_yesterdays_articles(self):
        pass
    
    def scrape_page(self,page) -> None:
        articles = self.get_json_by_date(page=page,date=date.today())
        self.current_page = articles["list"]

    def scrape_articles_from_page(self):
        page = 1
        while True:
            self.scrape_page(page)
            print(self.current_page)
            if self.current_page:
                page += 1
                for a in self.current_page:
                    article = {
                        "portal":self.portal_id,
                        "title":a["cim"],
                        "lead":a["ajanlo"] if "ajanlo" in a else "",
                        "image":a["kep_1x1"] if "kep_1x1" in a else "",
                        "author": "",
                        "url":a["url"],
                        "category":a["rovat"],
                        "full_text": "",
                        "date": ""
                    }
                    #print(article)
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
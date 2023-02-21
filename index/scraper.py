from datetime import date, datetime, timedelta
from typing import List
from bs4 import Tag
import requests

from base.utils import get_html_from_url

from .config import conf

class IndexScraper:
    def __init__(self):
        self.base_url=conf["BASE_URL"], 
        self.portal_name=conf["PORTAL_NAME"],
        self.portal_id=conf["PORTAL_ID"]       


    def get_json_by_date(self,from_date:date,to_date:date,page:int=1):
        from_date_string = from_date.strftime('%Y-%m-%d') 
        to_date_string = to_date.strftime('%Y-%m-%d') 
        url = "https://index.hu/api/json/"
        headers = {
            "Referer": f"https://index.hu/24ora/?tol={from_date_string}&ig={to_date_string}",      
            }

        payload = {
            "rovat":"24ora",
            "url_params[alllowRovatChoose]": 1,
            "url_params[pepe]": 1,
            "url_params[tol]": from_date_string,
            "url_params[ig]": to_date_string,
            "url_params[p]": page,
        }
        response = requests.get(url, params=payload,headers=headers)
        return response.json()
    
    def scrape_yesterdays_articles(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        self.scrape_articles_from_page_by_date(yesterday,yesterday)

        return
    
    def scrape_page(self,page:int,from_date:date,to_date:date) -> List[dict]:
        articles = self.get_json_by_date(page=page,from_date=from_date,to_date=to_date)
        return articles["list"]

    def scrape_articles_from_page_by_date(self,from_date:date,to_date:date):
        page = 0
        article_list = []
        while True:
            current_list = self.scrape_page(page,from_date,to_date)
            
            if current_list:
                page += 1
                for a in current_list:
                    article = {
                        "portal":self.portal_id,
                        "title":a["cim"],
                        "lead":a["ajanlo"] if "ajanlo" in a else "",
                        "image":a["kep_1x1"] if "kep_1x1" in a else "",
                        "author": "",
                        "url":a["url"],
                        "category":a["rovat"],
                        "full_text": "",
                        "date": datetime.fromtimestamp(a["ts"])
                    }
                    article_list.append(article)
            else:
                print(article_list)
                print(len(article_list))
                return article_list
            

    def scrape_author(self,url:str) -> str:
        soup = get_html_from_url(url)
        htmls = soup.select(".cikk-törzs")
        string = ""
        for h in htmls:
            string += f"\n{h.get_text()}"
        
        return string.strip()

    def scrape_full_text(self):
        pass


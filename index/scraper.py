from datetime import date, datetime, timedelta
import time
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
        self.detail_soup = None

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
                        "author": self.scrape_author(a["url"]),
                        "url":a["url"],
                        "category":a["rovat"],
                        "full_text": "",
                        "date": datetime.fromtimestamp(a["ts"])
                    }
                    article_list.append(article)
            else:
                #print(article_list)
                print(len(article_list))
                return article_list
            

    def scrape_author(self,url:str) -> str:
        is_loaded = False
        start_time = time.time()
        while not is_loaded:
            res = requests.get(url)
            print(res.status_code)
            detail_soup = get_html_from_url(url)
            if not len(detail_soup.contents) == 0:
                is_loaded = True
                self.detail_soup = detail_soup
            else:
                print("waiting")
                
                time.sleep(1)  # wait for 1 second before trying again
                elapsed_time = time.time() - start_time
                if elapsed_time > 10:  # set a timeout of 10 seconds
                    print("Timeout occurred")
                    break

        print(type(detail_soup))
        author = "Nincs szerző"
        #mindeközben,percrol perce
        try:
            authors = self.detail_soup.select(".name a")
            if not authors:
                raise Exception("No authors found")
            
            author = authors[0].get_text().strip()

        except Exception as e:
            authors = self.detail_soup.select(".szerzo a")
            if authors:
                if len(authors) == 1:
                    author = authors[0].get_text().strip()
                else:
                    author = authors[1].get_text().strip()   
        print("------------------------")
        print(url)      
        print(author)
        print("------------------------")
        return 

    def scrape_full_text(self,url:str):
        soup = get_html_from_url(url)
        htmls = soup.select(".cikk-törzs")
        string = ""
        for h in htmls:
            string += f"\n{h.get_text()}"
        
        return string.strip()


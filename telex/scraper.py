import requests
import openai

from bs4 import BeautifulSoup,Tag
from datetime import datetime,date, timedelta
from typing import List,Dict,Union

from db.client import MongoClient
from .utils import convert_to_dict

openai.api_key = "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"

def get_element_text(item, selector):
    element = item.select_one(selector)
    if element:
        return element.text.strip()
    else:
        return ""


class TelexScraper(MongoClient):
    def __init__(self):
        super().__init__()
        self.month_map = {
            "január": "January",
            "február": "February",
            "március": "March",
            "április": "April",
            "május": "May",
            "június": "June",
            "július": "July",
            "augusztus": "August",
            "szeptember": "September",
            "október": "October",
            "november": "November",
            "december": "December",
        }
        self.base_url = "https://telex.hu"
        self.db = self.client["newsData"]
        self.collection = self.db['articles']

    def get_html_from_url(self, url:str) -> str:
        # Send an HTTP request to the website and save the response
        response = requests.get(url)

        # Parse the HTML of the web page
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup

    def scrape_page(self, page: int = 1, save_to_bd:bool = False) -> List[dict]:
        url = f"{self.base_url}/archivum?oldal={page}"

        soup = self.get_html_from_url(url)

        # Find all the elements with the class `list__item` and `article`
        item_elements = soup.find_all('div', {"class": ["list__item", "article"]})

        articles = self.scape_items(item_elements)
        #save
        if save_to_bd:
            self.save_to_collection(articles)

        return articles

    def get_sentiment_analysis(self,title):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{title}\nmake a sentiment analysis  of the above title using this format: positive: 0.00;neutral: 0.00;negative:0.00\n0.00 is the percentage and the value should be between 0 and 1",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text = response.choices[0].text.strip()
        print("text i got: ",text, "\ntype: ", type(text))

        # Parse the string into a dictionary
        sentiment = convert_to_dict(text)
        print(sentiment)
        return

    def scape_items(self, item_elements: List[Tag]) -> List[Dict[str, Union[str, datetime]]]:
        articles = []

        date_format = "%Y. %B %d. – %H:%M"
        # Iterate over the item elements
        for item in item_elements:
            # Find the element containing the title
            title = get_element_text(item, 'a.list__item__title > span')
            author = get_element_text(item, 'div.article_date > em > a')
            lead = get_element_text(item, 'p.list__item__lead')
            date_string = get_element_text(item, 'div.article_date > span')

            title_element = item.select_one('a.list__item__title')
            if title_element:
                link = title_element['href']
            else:
                link = ""

            tag = get_element_text(item, 'div.tag--basic')


            for hungarian, english in self.month_map.items():
                date_string = date_string.replace(hungarian, english)

            item = {
                "portal":"telex",
                "title":title,  
                "lead":lead,
                "author": author,
                "url":f"{self.base_url}{link}",
                "category": tag,
                "full_text": self.get_full_text_from_article(f"{self.base_url}{link}"),
            }

            try:
                item["date"] = datetime.strptime(date_string, date_format)
            except:
                item["date"] = datetime.strptime(date_string, "%B %d. %Y. – %I:%M %p")

            articles.append(item) 
        
        return articles

    def get_full_text_from_article(self, url:str) -> str:
        # Parse the HTML of the web page
        soup = self.get_html_from_url(url)
        htmls = soup.select(".article-html-content")
        string = ""
        for h in htmls:
            string += h.get_text()
        
        return string.strip()

    def scrape_from_page_to_page(self,from_page:int,to_page:int) -> None:
        sum = 0
        for page in range(from_page,to_page):
            articles = self.scrape_page(page)
            sum += len(articles)
            print(articles)
            print("scraped page number: ", page)
            print("all scraped articles: ", sum)
            
        return

    def scrape_yesterdays_articles(self,current_page:int = 1):
        today = date.today()
        yesterday = today - timedelta(days=1)

        articles = self.scrape_page(current_page,False)
        articles_yesterday = [a for a in articles if a["date"].date() == yesterday]

        last_date = articles[-1]["date"].date()

        if len(articles_yesterday) > 0:
            self.save_to_collection(articles_yesterday)

        print("last date: ",last_date)
        if last_date == today or last_date == yesterday:
            self.scrape_yesterdays_articles(current_page + 1)

        return
        
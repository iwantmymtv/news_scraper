import requests
import openai

from bs4 import BeautifulSoup,Tag
from datetime import datetime
from typing import List,Dict,Union

from db.client import MongoClient
from .utils import convert_to_dict

openai.api_key = "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"

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

    def scrape_page(self, page: int = 1) -> List[dict]:
        url = f"{self.base_url}/archivum?oldal={page}"

        soup = self.get_html_from_url(url)

        # Find all the elements with the class `list__item` and `article`
        item_elements = soup.find_all('div', {"class": ["list__item", "article"]})

        articles = self.scape_items(item_elements)
        #save
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
            title_element = item.select_one('a.list__item__title > span')
            title = title_element.text.strip() if title_element else ""

            author_element = item.select_one('div.article_date > em > a')
            author = author_element.text.strip() if author_element else ""

            lead_element = item.select_one('p.list__item__lead')
            lead = lead_element.text.strip() if lead_element else ""

            date_element = item.select_one('div.article_date > span')
            date_string = date_element.text.strip() if date_element else ""

            title_element = item.select_one('a.list__item__title')
            link = title_element['href'] if lead_element else ""
            
            tag_element = item.select_one('div.tag--basic')
            tag = tag_element.text.strip() if title_element else ""


            for hungarian, english in self.month_map.items():
                date_string = date_string.replace(hungarian, english)

            item = {
                "portal":"telex",
                "title":title,  
                "lead":lead,
                "author": author,
                "url":f"{self.base_url}{link}",
                "category": tag,
                "full_text": self.get_full_text_from_article(f"{self.base_url}{link}")
            }

            try:
                item["date"] = datetime.strptime(date_string, date_format)
            except:
                item["date"] = datetime.strptime(date_string, "%B %d. %Y. – %I:%M %p")

            articles.append(item) 
        
        return articles

    def get_full_text_from_article(self, url:str) -> str:
        response = requests.get(url)
        # Parse the HTML of the web page
        soup = BeautifulSoup(response.text, 'html.parser')
        htmls = soup.select(".article-html-content")
        string = ""
        for h in htmls:
            string += h.get_text()
        
        return string.strip()

    def save_to_collection(self,items) -> None:
        for item in items:
            self.collection.update_one(
                item,
                {'$set': item},
                upsert=True
            )
        return

    def scrape_from_page_to_page(self,from_page:int,to_page:int) -> None:
        sum = 0
        for page in range(from_page,to_page):
            articles = self.scrape_page(page)
            sum += len(articles)
            print("scraped page number: ", page)
            print("all scraped articles: ", sum)
            
        return
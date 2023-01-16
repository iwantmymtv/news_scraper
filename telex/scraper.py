from datetime import datetime,date,timedelta
from typing import List,Dict

from bs4 import Tag

from base.scraper import Scraper
from base.utils import get_html_from_url,get_element_text
from db.django import upload_many

from .utils import to_datetime
class TelexScraper(Scraper):
    def __init__(self):
        Scraper.__init__(self, base_url="https://telex.hu", portal_name="telex",portal_id=1)
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

    def scrape_yesterdays_articles(self,current_page:int = 1) -> None:
        today = date.today()
        yesterday = today - timedelta(days=1)

        articles = self.scrape_page(current_page,False)
        
        articles_yesterday = [a for a in articles if to_datetime(a["date"]).date() == yesterday]

        last_date = to_datetime(articles[-1]["date"]).date()

        if len(articles_yesterday) > 0:
            upload_many(articles_yesterday)

        print("last date: ",last_date)
        if last_date == today or last_date == yesterday:
            self.scrape_yesterdays_articles(current_page + 1)

        return
        
    def scrape_title(self,soup:Tag) -> str:
        return get_element_text(soup, 'a.list__item__title > span')

    
    def scrape_lead(self,soup:Tag) -> str:
        return get_element_text(soup, 'p.list__item__lead')

    
    def scrape_author(self,soup:Tag) -> str:
        return get_element_text(soup, 'div.article_date > em > a')

    
    def scrape_detail_url(self,soup:Tag) -> str:
        url = ""
        title_element = soup.select_one('a.list__item__title')
        if title_element:
            url = title_element['href']

        return f"{self.base_url}{url}"

    
    def scrape_full_text(self,soup:Tag) -> str:
        # Parse the HTML of the web page
        html = get_html_from_url(self.scrape_detail_url(soup))
        htmls = html.select(".article-html-content")
        string = ""
        for h in htmls:
            string += h.get_text()
        
        return string.strip()
        
    
    def scrape_date(self,soup:Tag) -> datetime:
        date = datetime.now()
        date_format_hu = "%Y. %B %d. – %H:%M"
        date_format_en = "%B %d. %Y. – %I:%M %p"
        date_string = get_element_text(soup, 'div.article_date > span').lower()

        for hungarian, english in self.month_map.items():
            date_string = date_string.replace(hungarian, english)

        try:
            date = datetime.strptime(date_string, date_format_hu)
        except:
            date = datetime.strptime(date_string, date_format_en)

        return date

    
    def scrape_category(self,soup:Tag) -> str:
        return get_element_text(soup, 'div.tag--basic')
    
    
    def scrape_image(self,soup:Tag) -> str:
        element = soup.select_one("a.list__item__image img")
        if element:
            return element.get('src').strip()
        else:
            return ""
    

    def scrape_page(self, page: int = 1, save_to_bd:bool = False) -> List[dict]:
        url = f"{self.base_url}/archivum?oldal={page}"

        soup = get_html_from_url(url)

        # Find all the elements with the class `list__item` and `article`
        item_elements = soup.find_all('div', {"class": ["list__item", "article"]})

        articles = self.scape_articles_from_page(item_elements)
        print("articles:", articles)
        #save
        if save_to_bd:
            upload_many(articles)

        return articles

    def scape_articles_from_page(self, item_elements: List[Tag]) -> List[Dict]:
        articles = []
        for i in item_elements:
            articles.append(self.scrape_single_article(i))
        return articles
    
    def scrape_from_page_to_page(self,from_page:int,to_page:int,save_to_db:bool=False) -> None:
        sum = 0
        for page in range(from_page,to_page):
            articles = self.scrape_page(page,save_to_db)
            sum += len(articles)
            print(articles)
            print("scraped page number: ", page)
            print("all scraped articles: ", sum)
            
        return
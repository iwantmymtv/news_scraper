from datetime import datetime,date,timedelta
from typing import List,Dict

from bs4 import Tag
from pandas import to_datetime

from base.scraper import Scraper
from base.utils import get_html_from_url,get_element_text
from db.django import upload_many

from .config import conf


class HvgScraper(Scraper):
    def __init__(self):
        Scraper.__init__(self, 
                         base_url=conf["BASE_URL"], 
                         portal_name=conf["PORTAL_NAME"],
                         portal_id=conf["PORTAL_ID"]
                         )
        self.categories = [
            "itthon",
            "idojaras",
            "vilag",
            "eurologus",
            "gazdasag",
            "zhvg",
            "ingatlan",
            "tudomany",
            "europoli",
            "uzleti-tippek",
            "tudomany",
            "velemeny",
            "velemeny.nyuzsog",
            "sport",
            "cegauto",
            "kkv",
            "kultura",
            "elet",
            "pszichologiamagazin",
            "hvgkonyvek",
        ]
        self.default_date = datetime.now()

    def scrape_yesterdays_articles(self) -> None:
        for category in self.categories:
            print("kategoria: ", category)
            self.scrape_yesterdays_articles_by_category(category=category)
        return

    def scrape_yesterdays_articles_by_category(self,current_page:int = 1,category:str ="itthon") -> None:
        today = date.today()
        yesterday = today - timedelta(days=1)

        articles = self.scrape_page(page=current_page,save_to_bd=False,category=category)
        print(articles)
        if not articles:
            return 
        
        articles_yesterday = [a for a in articles if to_datetime(a["date"]).date() == yesterday]

        last_date = to_datetime(articles[-1]["date"]).date()

        if len(articles_yesterday) > 0:
            upload_many(articles_yesterday)

        print("last date: ",last_date)
        if last_date == today or last_date == yesterday:
            self.scrape_yesterdays_articles_by_category(current_page + 1,category=category)
        
        return


    def scrape_page(self, page: int = 1, category:str = "itthon",save_to_bd:bool = False) -> List[dict]:
        url = f"{self.base_url}/{category}/{page}"

        soup = get_html_from_url(url)

        # Find all the elements with the class `list__item` and `article`
        item_elements = soup.select('div.column-articlelist > article.articlelist-element.clear')

        articles = self.scape_articles_from_page(item_elements)
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

    def scrape_title(self,soup:Tag) -> str:
        return get_element_text(soup, 'h2.heading-3 > a')

    
    def scrape_lead(self,soup:Tag) -> str:
        return get_element_text(soup, 'p.article-lead')

    
    def scrape_author(self,soup:Tag) -> str:
        return get_element_text(soup, 'span.info > span')

    
    def scrape_detail_url(self,soup:Tag) -> str:
        url = ""
        title_element = soup.select_one('h2.heading-3 > a')
        if title_element:
            url = title_element['href']
            if not url[0] == "/":
                url = f"/{url}"
        return f"{self.base_url}{url}"

    
    def scrape_full_text(self,soup:Tag) -> str:
        # Parse the HTML of the web page
        html = get_html_from_url(self.scrape_detail_url(soup))
        htmls = html.select(".article-main")
        string = ""
        for h in htmls:
            string += f"\n{h.get_text()}"
        
        return string.strip()
        
    
    def scrape_date(self,soup:Tag) -> datetime:
        #2023.02.15. 15:33:00
        date_format_hu = "%Y.%m.%d. %H:%M:%S"
        time_element = soup.select_one('span.info > time')
        date_string = time_element['title']
        
        try:
            date = datetime.strptime(date_string, date_format_hu)
        except:
            date = self.default_date
        
        return date

    
    def scrape_category(self,soup:Tag) -> str:
        return get_element_text(soup, 'span.info > a.uppercase')
    
    
    def scrape_image(self,soup:Tag) -> str:
        element = soup.select_one("div.image-holder img")
        if element:
            return element.get('src').strip()
        else:
            return ""

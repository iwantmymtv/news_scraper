from telex.scraper import TelexScraper
from origo.scraper import OrigoScraper

from telex.views import telex_multi_scraper

def main():
    #telex_multi_scraper(save=True)
    #telex = TelexScraper()
    #articles = telex.scrape_page(1,True)
    origo = OrigoScraper()
    articles = origo.scrape_page("20230110")
    print(articles)

if __name__ == '__main__':
    main()
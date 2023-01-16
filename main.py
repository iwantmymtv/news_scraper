from telex.scraper import TelexScraper
from origo.scraper import OrigoScraper

from telex.views import telex_multi_scraper

def main():
    #telex_multi_scraper(save=True)
    telex = TelexScraper()
    origo = OrigoScraper()
    telex.scrape_yesterdays_articles()
    origo.scrape_yesterdays_articles()
    #articles = origo.scrape_from_date_to_date("20220110","20220113")

if __name__ == '__main__':
    main()
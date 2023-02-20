from db.django import generate_ner_entities, generate_sentiments

from hu24.scraper import HU24Scraper
from hvg.scraper import HvgScraper
from index.scraper import IndexScraper
from telex.scraper import TelexScraper
from origo.scraper import OrigoScraper


def main():
    """telex = TelexScraper()
    origo = OrigoScraper()
    hu24 = HU24Scraper()
    hvg = HvgScraper()
    
    hu24.scrape_yesterdays_articles()
    telex.scrape_yesterdays_articles()
    origo.scrape_yesterdays_articles()
    hvg.scrape_yesterdays_articles()

    generate_sentiments()
    generate_ner_entities()"""
    ind = IndexScraper()
    ind.scrape_articles_from_page()
    

if __name__ == '__main__':
    main()
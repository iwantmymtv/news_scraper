from telex.scraper import TelexScraper
from telex.views import telex_multi_scraper

def main():
    telex_multi_scraper(save=True)
    #telex = TelexScraper()
    #articles = telex.scrape_page(1,True)

if __name__ == '__main__':
    main()
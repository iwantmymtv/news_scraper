from telex.scraper import TelexScraper

def main ():
    print("hellllo")
    telex = TelexScraper()
    articles = telex.scrape_from_page_to_page(1,20)
    #telex.scrape_yesterdays_articles()
if __name__ == '__main__':
    main()
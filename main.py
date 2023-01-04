from telex.scraper import TelexScraper

def main ():
    print("hellllo")
    telex = TelexScraper()
    articles = telex.scrape_from_page_to_page(4938,5035)
    #4938,3980
if __name__ == '__main__':
    main()
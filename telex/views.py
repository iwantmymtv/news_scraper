import threading
from .scraper import TelexScraper


class TelexThread(threading.Thread):
    def __init__(self, start_page:int, end_page:int,save_to_db:bool):
        super().__init__()
        self.start_page = start_page
        self.end_page = end_page
        self.save_to_db = save_to_db
    
    def run(self):
        telex = TelexScraper()
        telex.scrape_from_page_to_page(self.start_page, self.end_page,self.save_to_db)
        

def telex_multi_scraper(save:bool = False):
    threads = []
    chunk_size = 500
    num_chunks = 10
    
    for i in range(num_chunks):
        start_page = i*chunk_size+1
        end_page = (i+1)*chunk_size
        t = TelexThread(start_page, end_page,save)
        threads.append(t)
        t.start()
    
    # wait for all threads to finish
    for t in threads:
        t.join()


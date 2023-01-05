import pymongo

class MongoClient:
    def __init__(
        self,
        connect_url:str = "mongodb+srv://testuser:m9wxnVkFPGhHjbST@news.ue9crl2.mongodb.net/?retryWrites=true&w=majority",
    ):
        self.connect_url = connect_url
        self.client = pymongo.MongoClient(self.connect_url)

    def save_to_collection(self,items) -> None:
        for item in items:
            self.collection.update_one(
                item,
                {'$set': item},
                upsert=True
            )
        return


    


    






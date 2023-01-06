import pymongo

class MongoClient:
    def __init__(
        self,
        db_name:str,
        collection_name:str,
    ):
        self.connect_url = "mongodb+srv://testuser:m9wxnVkFPGhHjbST@news.ue9crl2.mongodb.net/?retryWrites=true&w=majority"
        self.client = pymongo.MongoClient(self.connect_url)
        self.db = self.client[db_name]
        self.connection = self.db[collection_name]

    def save_to_collection(self,items) -> None:
        for item in items:
            self.collection.update_one(
                item,
                {'$set': item},
                upsert=True
            )
        return


    


    






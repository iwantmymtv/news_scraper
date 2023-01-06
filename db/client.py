import pymongo
from decouple import config

class MongoClient:
    def __init__(
        self,
        db_name:str,
        collection_name:str,
    ):
        self.connect_url = config("MONGO_SERVER_URL")
        self.client = pymongo.MongoClient(self.connect_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_many_to_collection(self,items) -> None:
        for item in items:
            self.save_one_to_collection(item)
        return

    def save_one_to_collection(self,item) -> None:
        self.collection.update_one(
            item,
            {'$set': item},
            upsert=True
        )
        return
    


    






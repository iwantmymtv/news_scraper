from typing import Dict, List
from datetime import datetime

def to_datetime(date_string:str) -> datetime:
    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    return date_object

""" from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2') """

""" def update_embedding_in_array(objects:List[Dict], values:List, name:str) -> List[Dict]:
    for obj, value in zip(objects, values):
        obj[name] = value
    return objects

def add_embeddings(articles:List[Dict]) -> List[Dict]:
    sentences = [i["title"] for i in articles]
    print(sentences)
    #Sentences are encoded by calling model.encode()
    embeddings = model.encode(sentences)
    new_articles = update_embedding_in_array(articles,embeddings,"embeddings")
    return new_articles

 """
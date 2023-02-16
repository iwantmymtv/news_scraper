import json
import requests
from decouple import config

def upload_many(data):
    headers = {"X-API-Key": config("DJANGO_API"), "Content-Type": "application/json"}
    response = requests.post(f"{config('DJANGO_BASE_URL')}/api/v1/news/upload_many", headers=headers, data=json.dumps(data))
    return response

def generate_sentiments():
    headers = {"X-API-Key": config("DJANGO_API"), "Content-Type": "application/json"}
    requests.get(f"{config('DJANGO_BASE_URL')}/api/v1/news/generate_sentiments", headers=headers)
    return 

def generate_ner_entities():
    headers = {"X-API-Key": config("DJANGO_API"), "Content-Type": "application/json"}
    requests.get(f"{config('DJANGO_BASE_URL')}/api/v1/news/generate_ner_entities", headers=headers)
    return 

def get_portal_id(portal_name:str) -> int:
    data = {
        "name": portal_name
    }
    headers = {"X-API-Key": config("DJANGO_API"), "Content-Type": "application/json"}
    response = requests.post(f"{config('DJANGO_BASE_URL')}/api/v1/news/get_potral_id", headers=headers, data=json.dumps(data))
    data = json.loads(response.content)
    return data["id"]

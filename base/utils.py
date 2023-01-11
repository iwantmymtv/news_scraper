from datetime import datetime
import requests
from bs4 import BeautifulSoup,ResultSet,Tag


# Convert a datetime object to a JSON-serializable string
def serialize_datetime(dt: datetime) -> str:
    return dt.isoformat()
    
def get_html_from_url(url: str) -> str:
    # Send an HTTP request to the website and save the response
    response = requests.get(url)
        # Parse the HTML of the web page
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def get_element_from_result_set(soup_list:ResultSet, selector:str) -> str:
    list = []
    for e in soup_list:
        list.append(get_element_text(e, selector))
    return list[0]

def get_element_text(soup:Tag, selector:str) -> str:
    element = soup.select_one(selector)
    if element:
        return element.text.strip()
    else:
        return ""
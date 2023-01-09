from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Convert a datetime object to a JSON-serializable string
def serialize_datetime(dt: datetime):
    return dt.strftime('%Y-%m-%d %H:%M:%S')
    
def get_html_from_url(url: str) -> str:
    # Send an HTTP request to the website and save the response
    response = requests.get(url)
        # Parse the HTML of the web page
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_element_text(soup, selector):
    element = soup.select_one(selector)
    if element:
        return element.text.strip()
    else:
        return ""
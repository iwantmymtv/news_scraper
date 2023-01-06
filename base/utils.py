import requests
from bs4 import BeautifulSoup


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
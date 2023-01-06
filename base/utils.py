import requests
from bs4 import BeautifulSoup

def get_html_from_url(url: str) -> str:
    # Send an HTTP request to the website and save the response
    response = requests.get(url)
        # Parse the HTML of the web page
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def convert_sentiment_string_to_dict(input_string:str) -> dict:
    parts = input_string.split(";")
    output_dict = {}
    for part in parts:
        key, value = part.split(":")
        output_dict[key.strip().lower()] = float(value.strip())
    return output_dict

def get_element_text(soup, selector):
    element = soup.select_one(selector)
    if element:
        return element.text.strip()
    else:
        return ""
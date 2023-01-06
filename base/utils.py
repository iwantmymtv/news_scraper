import openai
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

translator = Translator()
openai.api_key = "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"

def translate_to_english(sentence:str) -> str:
    translated = translator.translate(sentence, dest="en")
    return translated.text

def get_sentiment_analysis(title):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{title}\nmake a sentiment analysis  of the above title using this format: positive: 0.00;neutral: 0.00;negative:0.00\n0.00 is the percentage and the value should be between 0 and 1",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text = response.choices[0].text.strip().replace("\n","")
    print("text i got: ",text, "\ntype: ", type(text))

    # Parse the string into a dictionary
    sentiment = convert_sentiment_string_to_dict(text)
    return sentiment

def get_html_from_url(url: str) -> str:
    # Send an HTTP request to the website and save the response
    response = requests.get(url)
        # Parse the HTML of the web page
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def convert_sentiment_string_to_dict(input_string:str) -> dict:
    parts = input_string.split(";")
    positive = parts[0].split(":")
    neutral = parts[1].split(":")
    negative = parts[2].split(":")

    output_dict = {
        "positive": None,
        "neutral": None,
        "negative": None
    }

    if positive and len(positive) == 2:
        output_dict["positive"] = float(positive[1].strip())

    if neutral and len(neutral) == 2:
        output_dict["neutral"] = float(neutral[1].strip())
        
    if negative and len(negative) == 2:
        output_dict["negative"] = float(negative[1].strip())

    print(output_dict)
    return output_dict

def get_element_text(soup, selector):
    element = soup.select_one(selector)
    if element:
        return element.text.strip()
    else:
        return ""
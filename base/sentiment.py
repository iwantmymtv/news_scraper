import six

from google.cloud import language_v1
#from google.oauth2.credentials import Credentials
from google.auth.api_key import Credentials

from decouple import config


creds = Credentials(config("GOOGLE_API_KEY"))

def title_analyze_sentiment(content):

    client = language_v1.LanguageServiceClient(credentials=creds)
    
    print(len(content))

    if isinstance(content, six.binary_type):
        content = content.decode("utf-8")

    type_ = language_v1.Document.Type.PLAIN_TEXT
    document = {"type_": type_, "content": content}

    response = client.analyze_sentiment(request={"document": document})
    sentiment = response.document_sentiment
    print("Score: {}".format(sentiment.score))
    print("Magnitude: {}".format(sentiment.magnitude))

content = 'On the fourth day of voting in the House of Representatives, McCarthy is just a few votes short of the Speakership'
title_analyze_sentiment(content)
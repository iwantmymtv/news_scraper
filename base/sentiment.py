# import the Google Cloud Natural Language API client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# create a client for interacting with the Cloud Natural Language API
client = language.LanguageServiceClient()

# specify the text you want to analyze
text = 'I am feeling very happy today!'

# build a document object representing the text
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT
)

# detect the sentiment of the text
sentiment = client.analyze_sentiment(document=document).document_sentiment

# print the sentiment score and magnitude
print('Score: {}'.format(sentiment.score))
print('Magnitude: {}'.format(sentiment.magnitude))
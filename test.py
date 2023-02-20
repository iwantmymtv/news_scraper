""" import sys
from pymilvus import connections
from pymilvus import Collection
from decouple import config

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

milvus_uri = config("MILVUS_URI")
user = config("MILVUS_USER")
password = config("MILVUS_PSWD")

connections.connect("default",
                    uri=milvus_uri,
                    user=user,
                    password=password,
                    secure=True)
                    
#Our sentences we like to encode
sentences = ['Orbán kijelölte a magyar középhatalmiság útját, ami zsibbasztó közhelyekkel van kikövezve',
    'Rendkívüli szünetet rendeltek el abban a szentgotthárdi iskolában, ahol 29 tanár kezdett polgári engedetlenségbe',
    'Jelenlegi formájában megszűnik a világ egyik legjobbjának tartott étterme, a dán Noma']

#Sentences are encoded by calling model.encode()
embeddings = model.encode(sentences)

#Print the embeddings
for sentence, embedding in zip(sentences, embeddings):
    print("Sentence:", sentence)
    print("Embedding:", type(embedding),embedding.shape)
    print("Size: ", sys.getsizeof(embedding)) """
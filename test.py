import sys
from pymilvus import connections
from pymilvus import Collection

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

milvus_uri = 
user = 
password = 
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
    print("Size: ", sys.getsizeof(embedding))
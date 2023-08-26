import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import random
import chromadb
import numpy as np

np.set_printoptions(precision=6, suppress=True)
model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')

df = pd.read_csv('../data/chatbot/ChatbotData.csv')
df1 = pd.read_csv('../data/chatbot/embeding.csv', header=None)


client = chromadb.Client()
collections = client.create_collection('chatbot')

embeddings = []
metadata = []
ids = []

for temp in range(len(df1)):
    ids.append(str(temp+1))
    embeddings.append(df1.iloc[temp].tolist())
    metadata.append({'A': df.iloc[temp]['A']})

collections.add(embeddings=embeddings, metadatas=metadata, ids=ids)


def chatbot_qa(text):
    chat_text = model.encode(text)
    query_result = collections.query(query_embeddings=[chat_text.tolist()], n_results=3)
    return query_result['metadatas'][0][0]['A']


print(chatbot_qa('하하'))
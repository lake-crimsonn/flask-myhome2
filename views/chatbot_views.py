import pandas as pd

from flask import Blueprint, render_template, request, url_for, redirect
from sentence_transformers import SentenceTransformer
import chromadb


bp = Blueprint('chatbot', __name__, url_prefix='/chatbot')

model = SentenceTransformer(
    'sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')

df = pd.read_csv('data/chatbot/ChatbotData.csv')
df1 = pd.read_csv(
    'data/chatbot/embeding.csv', header=None)

client = chromadb.Client()
collections = client.create_collection('chatbot')

embeddings = []
metadata = []
ids = []
data_arr = []

for temp in range(len(df1)):
    ids.append(str(temp+1))
    embeddings.append(df1.iloc[temp].tolist())
    metadata.append({'A': df.iloc[temp]['A']})

collections.add(embeddings=embeddings, metadatas=metadata, ids=ids)


@bp.route('/')
def chatbot_main():

    no_message = "아무런 메세지가 없습니다."
    if not data_arr:
        data_arr.append(no_message)
    elif no_message in data_arr:
        data_arr.remove(no_message)

    return render_template('chatbot.html', chat_data=data_arr)


@bp.route('/post', methods=['POST'])
def chatbot_post():
    data_arr.append(request.form['send_message'])
    print(request.form['send_message'])

    infer_message = chatbot_gen(request.form['send_message'])
    data_arr.append(infer_message)
    return redirect(url_for('chatbot.chatbot_main'))


def chatbot_gen(text):

    chat_text = model.encode(text)
    query_result = collections.query(
        query_embeddings=[chat_text.tolist()], n_results=3)

    return query_result['metadatas'][0][0]['A']

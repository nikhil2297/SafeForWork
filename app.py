from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np 
from sklearn.preprocessing import StandardScaler
import keras
import json
import re
import string
import nltk
import os
from nltk.corpus import stopwords

nltk.download('stopwords')


app = Flask(__name__)

load_model = keras.models.load_model(os.getcwd() + "/notebook/model.h5")
with open(os.getcwd() + '/notebook/tokenizer.pickle', 'rb') as handle:
    load_tokenizer = pickle.load(handle)

result = {};

@app.route('/')
def index() :
    return render_template('index.html')

def replace_hashtags(text):
    words = text.split()
    for i, word in enumerate(words):
        if word.startswith('#'):
            words[i] = f'<span class="blue-color">{word}</span>'
    return ' '.join(words)

def replace_at_words(text) :
    return re.sub(r'@(\w+)', r'<span class="username-color">@\1</span>', text)

def update_json() :
    if(os.path.exists('updated_data.json')) :
        with open('updated_data.json') as file:
            data = json.load(file)
    else :
        with open(os.getcwd() + '\data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)


        for tweet in data :
            tweet['sentiment'] = float(predict_sentiment(tweet['tweet']))
            tweet['tweet'] = replace_at_words(replace_hashtags(tweet['tweet']))
    
    return data;


@app.route('/tweets')
def navigateToTweets() :
    # with open('updated_data.json', 'r') as file:
    #     data = json.load(file)
    
    # return jsonify(data)

    return render_template('tweet.html', comments=update_json())

def addTweets(tweet) :
    tweet['sentiment'] = predict_sentiment(tweet['tweet'])

    return tweet

def clean_text(text) : 
    text = str(text).lower()
    text = re.sub('', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)

    stopword = set(stopwords.words('english'))
    stemmer = nltk.SnowballStemmer("english")
    text = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(text)
    return text

def predict_sentiment(text) :
    text = [clean_text(text)]
    text = load_tokenizer.texts_to_sequences(text)
    text = keras.preprocessing.sequence.pad_sequences(text, maxlen=300)
    prediction = load_model.predict(text)
    return prediction

if __name__ == '__main__':
    app.run(debug=True)
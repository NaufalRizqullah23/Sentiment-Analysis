import snscrape.modules.twitter as sntwitter
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from joblib import load
from flask import Flask, render_template, request
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

model = load('sentiment_analysisV2.pkl')
vectorizer = load('vectorizer.pkl')

stop_words = StopWordRemoverFactory().get_stop_words()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    query = request.form['text']
    max_tweets = 10

    scraped_tweets = []

    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if len(scraped_tweets) == max_tweets:
            break
        else:
            scraped_tweets.append(tweet.content)
    # for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query + 'lang:id').get_items()):
    #     if i >= max_tweets:
    #         break
    #     scraped_tweets.append(tweet.content)

    X = vectorizer.transform(scraped_tweets)

    results = []

    for i, tweet in enumerate(scraped_tweets):
        sentiment = model.predict(X[i])
        results.append((tweet, sentiment[0]))
    return render_template('result.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)

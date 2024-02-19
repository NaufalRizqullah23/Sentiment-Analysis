from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import load, dump
from flask import Flask, render_template, request, jsonify
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from collections import Counter
import asyncio
from twscrape import API
import json
import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from imblearn.over_sampling import SMOTE
from sklearn.naive_bayes import MultinomialNB
import numpy as np

model = load('sentiment_analysisV2.pkl')
vectorizer = load('vectorizer.pkl')
df = pd.read_csv('full_dataset.csv')
stop_words = StopWordRemoverFactory().get_stop_words()

app = Flask(__name__)

tw_api = API()


async def add_and_log_in_accounts():
    await tw_api.pool.add_account("Sinopla23", "Sandalbutut23.", "dajoka23@gmail.com", "Sandalbutut23.")
    await tw_api.pool.login_all()


def preprocess_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\S+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('indonesian'))
    tokens = [token for token in tokens if token not in stop_words]

    # stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    tokens = [stemmer.stem(token) for token in tokens]

    # join token into sentence
    text = ' '.join(tokens)
    return text

# async def fetch_tweets(query, max_tweets):


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    query = request.form['text']
    full_query = query + " lang:id"
    max_tweets = 10

    scraped_tweets = []

    async def fetch_tweets(query, limit):
        await add_and_log_in_accounts()
        async for tweet in tw_api.search(query, limit=limit):
            scraped_tweets.append(tweet.rawContent)

    asyncio.run(fetch_tweets(full_query, max_tweets))

    X = vectorizer.transform(scraped_tweets)

    results = []

    for i, tweet in enumerate(scraped_tweets):
        sentiment = model.predict(X[i])
        predicted_sentiment = int(sentiment[0])
        results.append((tweet, predicted_sentiment))

        label_dict = {-1: 'NEGATIF', 0: 'NETRAL', 1: 'POSITIF'}
        labeled_results = [label_dict[result[1]] for result in results]
        sentiment_count = Counter(labeled_results)

        most_common_sentiment = sentiment_count.most_common(1)[0][0]
    return render_template('result.html', results=results, most_common_sentiment=most_common_sentiment, query=query)


@app.route('/feedback', methods=['POST'])
def feedback():
    data = json.loads(request.data.decode('utf-8'))

    tweet = data['tweet']
    predicted_sentiment = int(data['predicted_sentiment'])
    feedback = int(data['feedback'])

    print(
        f"Received feedback for tweet: '{tweet}', Predicted Sentiment: '{predicted_sentiment}', Feedback: '{feedback}'")

    # preprocess tweet feedback
    preprocessed_tweet = preprocess_text(tweet)

    # update dataset
    global df
    new_entry = {'Date': '', 'Username': '',
                 'Tweet': preprocessed_tweet, 'label': feedback}
    df = df.append(new_entry, ignore_index=True)
    df['Tweet'].fillna('', inplace=True)

    # Save New Dataset
    df.to_csv('full_dataset.csv', index=False)

    df = pd.read_csv('full_dataset.csv')
    df['Tweet'] = df['Tweet'].replace(np.nan, '')
    df.dropna(inplace=True)

    # retrain the model
    X = df['Tweet']
    y = df['label']
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=50000)
    X_vec = vectorizer.fit_transform(X)

    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X_vec, y)

    nb = MultinomialNB(alpha=1)
    nb.fit(X_resampled, y_resampled)

    # save the updated model
    dump(nb, 'sentiment_analysisV2.pkl')
    dump(vectorizer, 'vectorizer.pkl')

    print("model update success!")

    # Return a response to acknowledge the feedback
    response_data = {'message': 'Model updated successfully'}
    return jsonify(response_data), 200


if __name__ == '__main__':
    app.run(debug=True)

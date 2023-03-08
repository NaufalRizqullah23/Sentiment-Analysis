import pandas as pd
import string
import re
import nltk
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

df = pd.read_csv('thedataset2.csv', encoding='ISO-8859-1')


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

    # join tokens to form sentence
    text = ' '.join(tokens)
    return text


# apply the preprocessing to 'Tweet' column
df['Tweet'] = df['Tweet'].apply(preprocess_text)

# save the dataset to CSV file
df.to_csv('pre_dataset2.csv', index=False)

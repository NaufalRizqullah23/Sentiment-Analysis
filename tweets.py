import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "(@PendisKemenag)"
query2 = "(to:PendisKemenag) (@PendisKemenag)"
tweets = []
limit = 10000

for tweet in sntwitter.TwitterSearchScraper(query).get_items():

    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.user.username, tweet.content])

df = pd.DataFrame(tweets, columns=['Date', 'Username', 'Tweet'])

filename = 'onlypendis.csv'

df.to_csv(filename, index=False)

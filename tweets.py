import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "(@PendisKemenag)"
query2 = "(to:PendisKemenag) (@PendisKemenag)"
query3 = "Moderasi Beragama until:2023-02-16 since:2022-01-01"
tweets = []
limit = 10000

for tweet in sntwitter.TwitterSearchScraper(query3).get_items():

    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.user.username, tweet.content])

df = pd.DataFrame(tweets, columns=['Date', 'Username', 'Tweet'])

filename = 'moderasiberagama.csv'

df.to_csv(filename, index=False)

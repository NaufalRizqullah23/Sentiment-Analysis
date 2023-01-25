import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "(@PendisKemenag) until:2023-01-25 since:2022-01-01"
tweets = []
limit = 10000

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    # print(vars(tweet))
    # break

    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.user.username, tweet.content])

df = pd.DataFrame(tweets, columns=['Date', 'Username', 'Tweet'])

filename = 'Scrape.csv'

df.to_csv(filename, index=False)

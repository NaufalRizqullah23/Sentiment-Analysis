import snscrape.modules.twitter as sntwitter
import csv

# Set the query and user to search
query = "PendisKemenag"
user = "PendisKemenag"

# Create a csv file to store the results
csvFile = open('test2.csv', 'a', newline='', encoding='utf8')
csvWriter = csv.writer(csvFile)

# Set the limit to 10,000 tweets
max_tweets = 10000
tweet_count = 0

# Iterate through top-level tweets and their replies
for tweet in sntwitter.TwitterSearchScraper(f'{query}').get_items():
    if tweet.user.username == user:
        csvWriter.writerow([tweet.id, tweet.date, tweet.content, ""])
        for reply in sntwitter.TwitterSearchScraper(f'"{tweet.url}"').get_items():
            if reply.inReplyToTweetId == tweet.id:
                csvWriter.writerow([reply.id, reply.date, "", reply.content])
        tweet_count += 1
        if tweet_count >= max_tweets:
            break

# Close the csv file
csvFile.close()

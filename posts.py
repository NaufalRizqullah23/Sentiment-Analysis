import facebook
import requests
import csv

# Get your Access Token from Facebook Developer
access_token = 'EAAR2De0jbC4BAKVVvEGcjrGnZCbqgywTASUlkHyPo4UoR60oHDmQmJRhZB56ZBgl2jx0TT9hxBfjUTx5zZAJI4ZApgc5fnEGu2wraXxhTOHiJ20KJZCghtc0xeXzlib7T8ZBRgUgmAT742Bc2KRu8VduZC19KGUZCLjPMSjeKnqey06vhbrynKNPfPXIabPZAeHZB4x5sjTQuiRCDbzpvgpnzxu'

# Initialize the Facebook Graph API
graph = facebook.GraphAPI(access_token)

# Define the Facebook Page ID
page_id = '110397838639459'

# Get the posts from the page
posts = graph.get_connections(id=page_id, connection_name='posts')

# Create a CSV file
with open('comments.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Post ID', 'Comment Message'])

    # Loop through all the posts
    for post in posts['data']:
        post_id = post['id']
        comments = graph.get_connections(
            id=post_id, connection_name='comments')

        # Loop through all the comments of the post
        for comment in comments['data']:
            writer.writerow([post_id, comment['message']])

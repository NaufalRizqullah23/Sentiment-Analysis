import facebook
import requests
import csv

# Get your Access Token from Facebook Developer
access_token = 'EAAR2De0jbC4BAKw2sHRZBzYqcR3ZAH95kZCX3Mir55PJhmVMrYXMAlVhDQJf4lSKYz9r0w2o5SBakwf4UrxHHz1HZAkEOKiVZBWx93J4YvZAsnYSDvdELyhQnI2t1pZCBg3kBKOwrGqCKf8SBKhnDtL6NC9pZA7U6EeXfgeIwOphFQDXv4mP0rVVJXlimJnNj2iU1Egp6QkPKhKUGDZAp25lS'

# Initialize the Facebook Graph API
graph = facebook.GraphAPI(access_token)

# Define the Facebook Page ID
page_id = '110397838639459'

# Get the posts from the page
posts = graph.get_connections(id=page_id, connection_name='posts')

# Create a CSV file
with open('postscomments.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Post ID', 'Post Message',
                    'Comment ID', 'Comment Message'])

    # Loop through all the posts
    for post in posts['data']:
        post_id = post['id']
        post_message = post.get('message', '')
        comments = graph.get_connections(
            id=post_id, connection_name='comments')

        # Loop through all the comments of the post
        for comment in comments['data']:
            writer.writerow(
                [post_id, post_message, comment['id'], comment['message']])

import facebook
import requests
import csv

# Get your Access Token from Facebook Developer
access_token = 'EAAR2De0jbC4BANqcoEM5IhylB1GoKyikwhEDs4gOg2oHfUmrSzn4ylgkKjHMOBm2OuXYH35LzfCm3aUGxLdUOrTPTOvk8p4rGZBNYS1k8BlTKElpjRAYmlexDjhFVOpQF4pZBGgwNF95YuZCbqMjlekVZCZAZAtpfZC7OTPNFjLcuFtbK8Pjk47WHt86tWoVLIvotSyznEcPyGWkXTGTvxq'

# Initialize the Facebook Graph API
graph = facebook.GraphAPI(access_token)

# Define the Facebook Page ID
page_id = '110397838639459'

# Get the posts from the page
posts = graph.get_connections(id=page_id, connection_name='posts')

# Create a CSV file
with open('withlikes.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Post ID', 'Post Message', 'Likes',
                    'Comment ID', 'Comment Message'])

    # Loop through all the posts
    for post in posts['data']:
        post_id = post['id']
        post_message = post.get('message', '')
        likes = post.get('likes', {}).get('summary', {}).get('total_count', 0)
        comments = graph.get_connections(
            id=post_id, connection_name='comments')

        # Loop through all the comments of the post
        for comment in comments['data']:
            writer.writerow([post_id, post_message, likes,
                            comment['id'], comment['message']])

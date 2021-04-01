import requests
from ..models import *

def get_foreign_author(url,author_id): #can probably change url to node
    s = requests.Session()
    s.auth = ('root','root')
    res = s.get(url+author_id)
    author_info = res.json()
    new_author = Author()
    new_author.id = author_info['id']
    new_author.username = author_info['username']
    new_author.github_link = author_info['github_link']
    new_author.friends = author_info['friends']
    new_author.url = author_info['url']
    #this stuff is commented out because I have no idea how to work it
    # if author_info['following'] != '':
    #     for following in author_info['following']:
    #         new_author.following.set(following)
    # if author_info['followers'] != '':
    #     for follower in author_info['followers']:
    #         print(follower)
    #         new_author.followers.set(follower)
    return new_author

def get_foreign_posts(url): #can probably replace with node
    s = requests.Session()
    s.auth = ('root','root') #these will be node.username and node.password
    res = s.get(url+'posts/') #will need to add headers before here with .update({"blah": "true"})
    posts_new = []              #yeah s.get(url, headers={'BLAH': 'blah', 'host': 'heroku_url'})
    for item in res.json():
        new_post = Post()
        new_post.contents = item['contents']
        new_post.created_by = get_foreign_author(url+'author/', item['created_by'])
        new_post.created_at = item['created_at']
        posts_new.append(new_post)
    return posts_new

def get_foreign_comment(url, author_id, post_id): #example url 'http://hermes-cmput404.herokuapp.com/api/' but should be again a node
    s = requests.Session()
    s.auth = ('root','root')
    res = s.get(url+'author/'+author_id+"/posts/"+post_id+"/comments") #god I hope this path doesnt change
    comments = []
    for item in res.json():
        new_comment = Comment()
        #add things to things like other ones
    return comments
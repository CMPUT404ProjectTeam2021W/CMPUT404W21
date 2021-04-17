import requests
from ..models import *
from django.http import JsonResponse
from collections import OrderedDict
from requests.auth import HTTPBasicAuth
from ..serializers import *
from ..models import Server
from django.utils.dateparse import parse_datetime
import base64



def get_foreign_author(url,author_id): #can probably change url to node
    s = requests.Session()
    s.auth = ('root','root')
    res = s.get(url+author_id)
    author_info = res.json()
    new_author = Author()
    new_author.id = author_info['id']
    new_author.username = author_info['username']
    new_author.github = author_info['github']
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

def get_foreign_posts(origin): #can probably replace with node
    s = requests.Session()
    s.auth = ('chatbyte','jeremychoo') #these will be node.username and node.password
    headers = "Authorization: Basic "
    res = s.get(origin+'author/1/stream') #will need to add headers before here with .update({"blah": "true"})

    posts_new = []            #yeah s.get(url, headers={'BLAH': 'blah', 'host': 'heroku_url'})
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
def fix_git_datetime(git_list):
    for event in git_list:
        event['created_at'] = parse_datetime(event['created_at'])
    return git_list
    
def get_stream(request):

    servers = Server.objects.all()
    data_list = []
    post_list = []
    author_list = []
    for server in servers:

        url = server.hostname+'author/1/stream'
        headers = {'Origin': server.hostname, 'X-Request-User': str(server.hostname) + "author/" + '1' + "/"}

        response = JsonResponse({"Error": "Bad request"}, status=400)
        if request.method == "GET":
            response = requests.get(url, headers=headers, auth=HTTPBasicAuth(server.username, server.password))
        data = deserialize_json(response.json()["posts"], server)
        for posts in data[0]:
            post_list.append(posts)
        for authors in data[1]:
            author_list.append(authors)
    data_list.append(post_list)
    data_list.append(author_list)

    return data_list
import pprint
def deserialize_json(json_response, server):
    #x = PostDeserializer(json_response, many=True).data
    #from pprint import pprint
    #pprint(json_response[2])
    data_list = []
    temp = {}
    author_list = []
    post_list = []
    for obj_temp in json_response:

        new_post = Post()
        new_post.title = obj_temp["title"]
        new_post.description = obj_temp["description"]
        ind = obj_temp["id"].find('posts/')
        new_post.id = obj_temp["id"][ind+len('posts/'):]
        new_post.author = Author()
        new_post.author.url = obj_temp["author"]["id"]
        new_post.author.username = obj_temp["author"]["displayName"]
        new_post.author.github = obj_temp["author"]["github"]
        new_post.published = parse_datetime(obj_temp["published"])
        new_post.visibility = obj_temp["visibility"]
        new_post.categories = obj_temp["contentType"] #add ifs if their content type stuff is different than our catigores 
        if obj_temp["contentType"] == "image/jpg":
            new_post.categories = 'image/jpeg'
            new_post.description = obj_temp['content']
        if obj_temp['contentType'] == 'image/png':
            new_post.categories = "image/png"
            new_post.description = obj_temp['content']
        new_post.origin = obj_temp["origin"]

        get_index = obj_temp["author"]["id"].find('author/')
        check = obj_temp["author"]["id"][get_index+len('author/'):]

        if check not in temp:
            new_post.author.id = check
            temp[check] = check
            author_list.append(new_post.author)
        if check in temp:
            new_post.author.id = temp[check]
        post_list.append(new_post)

    data_list.append(post_list)
    data_list.append(author_list)

    return data_list


def deserialize_likes_json(json_response, post):
    likes_list = list()
    for like_json in json_response:
        new_like = Like()
        new_like.id = like_json['id']
        new_like.author = Author()
        get_index = like_json['author']['id'].find('author/')
        author_id = like_json["author"]["id"][get_index+len('author/'):]
        new_like.author.id = author_id
        new_like.author.username = like_json['author']['displayName']
        new_like.author.url = like_json['author']['id']
        new_like.author.github = like_json['author']['github']
        new_like.object = post
        likes_list.append(new_like)
    return likes_list




#adapted from: https://nemecek.be/blog/8/django-how-to-send-image-file-as-part-of-response
#Author: Filip Němeček https://twitter.com/nemecek_f
def image_as_post(image_path):
    try:
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            file_size = (len(image_data) * 6 - image_data.count('=') * 8) / 8
            max_size = 1 * 1024 * 1024 #1MB maybe smaller?
            if file_size > max_size:
                return 100 
        #check filesize in bits
        return image_data
    except:
        return 110
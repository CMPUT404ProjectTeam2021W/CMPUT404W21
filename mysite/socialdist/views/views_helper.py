import json

import requests
from ..models import *
from django.http import JsonResponse, Http404
from collections import OrderedDict
from requests.auth import HTTPBasicAuth
from ..serializers import *
from ..models import Server
from django.utils.dateparse import parse_datetime
import base64


def get_foreign_post(post_id):
    stream = get_stream()[0]

    for post in stream:
        if post.id == post_id :
            return post
    return Http404()


def send_comment(comment, post):
    hostname = "https://chatbyte.herokuapp.com/"
    url = hostname + "author/" + post.author.id + "/posts/" + post.id + "/comments"
    x_request_user = "http://hermes-cmput404.herokuapp.com/author/de2cde87-2ea5-4aa6-9eed-70bb0d09b79d"
    headers = {'Origin': "http://hermes-cmput404.herokuapp.com/", 'X-Request-User': x_request_user }
    response = JsonResponse({"Error": "Bad request"}, status=400)
    comment_serialized = CommentSerializer(comment, many=False).data
    data = {}
    print("url: {}".format(url))
    print("xrequest: {}".format(x_request_user))
    print("headers: {}".format(headers))
    data['content'] = comment_serialized['comment']
    data['contentType'] = comment_serialized['contentType']
    data=json.dumps(data)
    response = requests.post(url, data=json.dumps(data),headers=headers, auth=HTTPBasicAuth("chatbyte", "jeremychoo"))
    print(data)
    print(response)
    return response

def map_comment(comment_dict, post):


    comment_id_index = comment_dict["id"].find("comments/")
    new_comment = Comment()
    new_comment.id = comment_dict["id"][comment_id_index + len('comments/'):]
    new_comment.published = parse_datetime(comment_dict["published"])
    new_comment.comment = comment_dict["comment"]
    new_comment.origin = 'https://chatbyte.herokuapp.com/'
    new_comment.post = post
    new_comment.author = Author()
    new_comment.author.url = comment_dict["author"]["url"]
    new_comment.author.username = comment_dict["author"]["displayName"]
    new_comment.author.github = comment_dict["author"]["github"]
    author_id_index = comment_dict["author"]["id"].find("author/")
    new_comment.author.id = comment_dict["author"]["id"][author_id_index + len("author/"):]
    print(new_comment)
    return new_comment

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

    return new_author

def get_foreign_comment(post_id): #example url 'http://hermes-cmput404.herokuapp.com/api/' but should be again a node

    hostname = "http://chatbyte.herokuapp.com/"
    stream = get_stream()
    comments_list = []

    for post in stream[0]:

        if post.id == post_id:
            url = hostname + "author/" + post.author.id + "/posts/" + post_id + "/comments"
            headers = {'Origin': hostname, 'X-Request-User': url}
            response = JsonResponse({"Error": "Bad request"}, status=400)
            response = requests.get(url, headers=headers, auth=HTTPBasicAuth("chatbyte", "jeremychoo"))
            # print(response.content)
            for comment_dict in response.json()["comments"]:

                comment = map_comment(comment_dict , post)
                comments_list.append(comment)
            print(comments_list)
            return comments_list


def fix_git_datetime(git_list):
    for event in git_list:
        event['created_at'] = parse_datetime(event['created_at'])
    return git_list

def get_stream():

    servers = Server.objects.all()
    data_list = []
    post_list = []
    author_list = []
    for server in servers:

        url = server.hostname+'all_posts/'
        headers = {'Origin': server.hostname, 'X-Request-User': str(server.hostname) + "all_posts/"}

        response = JsonResponse({"Error": "Bad request"}, status=400)

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


def deserialize_friends_json(json_response):
    friends_list = list()
    for author_json in json_response:
        new_author = Author()
        get_index = author_json['id'].find('author/')
        author_id = author_json["id"][get_index + len('author/'):]
        new_author.id = author_id
        new_author.username = author_json['displayName']
        new_author.url = author_json['id']
        new_author.github = author_json['github']
        friends_list.append(new_author)
    return friends_list




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

def get_remote_likes(request, post_id):
    post = get_foreign_post(post_id)
    hostname = "https://chatbyte.herokuapp.com/"
    url = "https://chatbyte.herokuapp.com/author/" + str(post.author.id) + "/posts/" + str(post.id) + "/likes"
    headers = {'Origin': hostname, 'X-Request-User': str(hostname) + "author/" + '1' + "/"}
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth('chatbyte', 'jeremychoo'))
    likes_list = deserialize_likes_json(response.json(), post)
    likes_count = len(likes_list)
    liked = False
    for like in likes_list:
        if request.user == like.author:
            liked = True

    return (liked, likes_count)

import requests
from ..models import *
from django.http import JsonResponse
from collections import OrderedDict
from requests.auth import HTTPBasicAuth
from ..serializers import *
from ..models import Server
from django.utils.dateparse import parse_datetime


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

def deserialize_json(json_response, server):

    x = PostDeserializer(json_response, many=True).data
    data_list = []
    temp = {}
    author_list = []
    post_list = []
    for obj_temp in x:

        new_post = Post()
        new_post.title = obj_temp["title"]
        new_post.description = obj_temp["description"]
        new_post.id = obj_temp["id"]
        new_post.author = Author()
        new_post.author.url = obj_temp["author"]["url"]
        new_post.author.username = obj_temp["author"]["username"]
        new_post.author.github = obj_temp["author"]["github"]
        new_post.published = parse_datetime(obj_temp["published"])

        new_post.visibility = obj_temp["visibility"]
        new_post.categories = obj_temp["categories"]
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

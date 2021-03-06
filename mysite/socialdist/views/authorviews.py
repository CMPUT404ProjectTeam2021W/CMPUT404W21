from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from ..forms import CreatePostForm, ImageForm, AuthorCreationForm, CreateCommentForm, SettingChangeForm
from .views_helper import *
from .authenticationviews import *
from ..models import *
import requests

@login_required
def author_profile(request, author_id):
    origin = ''
    posts = []
    author_details = None
    friends_count = ''
    friends = ''
    friend_request_status = False
    user_name = ''

    try:
        author_details = Author.objects.get(id=author_id)
        posts = Post.objects.filter(**{'author': author_details}) | Post.objects.filter(**{'shared_by': author_details})
        posts = posts.order_by('-published')
        origin = 'host'
        user_name = Author.objects.get(id=author_id).github
        friends = author_details.friends.all()
        friend_status = author_details in friends
        friends_count = friends.count()

    except:
        posts = get_author_stream(author_id)[1]
        author_details = Author()
        remote_author = get_author_stream(author_id)[0]
        # author_details.id = author_id
        author_details.username = remote_author['displayName']
        author_details.url = remote_author['url']
        author_details.github = remote_author['github']
        user_name = author_details.github
        hostname = "https://chatbyte.herokuapp.com/"
        url = "https://chatbyte.herokuapp.com/author/" + str(author_id) + "/followers"
        headers = {'Origin': hostname, 'X-Request-User': str(hostname) + "author/" + '1' + "/"}
        response = requests.get(url, headers=headers, auth=HTTPBasicAuth('chatbyte', 'jeremychoo'))
        friends_list = deserialize_friends_json(response.json()['items'])
        friends_count = len(friends_list)
        friend_status = False
        for friend in friends_list:
            if request.user == friend:
                friend_status = True

    ''' to move back '''
    try:
        FriendRequest.objects.get(from_author=request.user, to_author=author_details)
        friend_request_status = True
    except FriendRequest.DoesNotExist:
        friend_request_status = False

    '''move back above'''

    post_likes_dict = {}
    post_id_dict = {}
    post_liked = {}
    shared_by = {}
    for post in posts:
        if origin == 'host':
            post_likes_dict[post] = Like.objects.filter(**{'object': post}).count()
            try:
                post_liked[post] = Like.objects.get(author=request.user, object=post)
            except Like.DoesNotExist:
                post_liked[post] = False
            post_id_dict[post] = post.id
            shared_by[post] = request.user in post.shared_by.all()
        else:
            hostname = "https://chatbyte.herokuapp.com/"
            url = "https://chatbyte.herokuapp.com/author/" + str(post.author.id) + "/posts/" + str(post.id) + "/likes"
            headers = {'Origin': hostname, 'X-Request-User': str(hostname) + "author/" + '1' + "/"}
            response = requests.get(url, headers=headers, auth=HTTPBasicAuth('chatbyte', 'jeremychoo'))
            likes_list = deserialize_likes_json(response.json(), post)
            post_likes_dict[post] = len(likes_list)
            post_liked[post] = False
            for like in likes_list:
                if request.user == like.author:
                    post_liked[post] = True
            post_id_dict[post] = post.id

    #adapted from https://simpleisbetterthancomplex.com/tutorial/2018/02/03/how-to-use-restful-apis-with-django.html
    #author Vitor Freitas
    user = {}

    if user_name != '' and user_name !=None:
        new_username = user_name.split('/')[-1]
        url = 'https://api.github.com/users/%s/events' % new_username
        response = requests.get(url)
        user = fix_git_datetime(response.json())

    return render(request, 'socialdist/author_profile.html', {'posts': post_likes_dict, 'author': author_details.username,
                                                              'post_liked': post_liked,
                                                              'author_id': author_id, 'friend_status': friend_status,
                                                              'friend_request_status': friend_request_status,
                                                              'friends_count': friends_count, 'post_id': post_id_dict,
                                                              'shared_by': shared_by, 'origin': origin, 'git_user': user})
#https://api.github.com/users/{username}/events


def send_friend_request(request, author_id):
    from_author = request.user
    to_author = Author.objects.get(id=author_id)
    friend_request, created = FriendRequest.objects.get_or_create(from_author=from_author, to_author=to_author)
    if (not created) or (to_author in from_author.friends.all()):
        return HttpResponse("Request already sent OR The author is your friend")
    else:
        return redirect(request.META['HTTP_REFERER'])


def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_author == request.user:
        friend_request.to_author.friends.add(friend_request.from_author)
        friend_request.from_author.friends.add(friend_request.to_author)
        friend_request.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse("The author does not have this request")


def reject_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_author == request.user:
        friend_request.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse("The author does not have this request")


def cancel_friend_request(request, author_id):
    to_author_obj = Author.objects.get(id=author_id)
    friend_request = FriendRequest.objects.get(to_author=to_author_obj)
    if friend_request.from_author == request.user:
        friend_request.delete()
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse("The author does not have this request")


def unfriend(request, author_id):
    from_author = request.user
    to_author = Author.objects.get(id=author_id)
    if to_author in from_author.friends.all():
        from_author.friends.remove(to_author)
        to_author.friends.remove(from_author)
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('You are not friends')

def friends(request, author_id):
    author_details = Author.objects.get(id=author_id)
    friends_list = author_details.friends.all()
    author_name = author_details.username
    return render(request, 'socialdist/friends.html', {'author': author_name, 'friends': friends_list})

#def github_settings(request):
#
#    if request.method == 'POST':
#        form = GithubChangeForm(request.POST, request.FILES)
#        if form.is_valid():
#            form.save(request.user.id)
#            return redirect(request.META['HTTP_REFERER'])
#
#    elif request.method == 'GET':
#        form = GithubChangeForm()
#        return render(request, 'socialdist/user_settings.html', {'form': form})
#
#    else:
#        return HttpResponseNotAllowed(['GET', 'POST'])

@login_required
def user_settings(request):

    if request.method == 'POST':
        form = SettingChangeForm(request.POST, request.FILES)
        if form.is_valid():
            setting_changed = form.save(request.user.id)
            if setting_changed:
                return redirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponse('required an author')

    elif request.method == 'GET':
        form = SettingChangeForm()
        return render(request, 'socialdist/user_settings.html', {'form': form})

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])



#adapted from https://simpleisbetterthancomplex.com/tutorial/2018/02/03/how-to-use-restful-apis-with-django.html
#author Vitor Freitas

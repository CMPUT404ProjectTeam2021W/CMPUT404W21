from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from ..forms import CreatePostForm, ImageForm, AuthorCreationForm, CreateCommentForm
from .views_helper import *
from .authenticationviews import *
from ..models import *


@login_required
def author_profile(request, author_id):
    origin = ''
    posts = []
    author_details = None
    friends_count = ''
    friends = ''
    friend_request_status = False
    try:
        author_details = get_object_or_404(Author, id=author_id)
        posts = Post.objects.filter(**{'author': author_details}) | Post.objects.filter(**{'shared_by': author_details})
        friends = request.user.friends.all()
        friend_status = author_details in friends
        try:
            FriendRequest.objects.get(from_author=request.user, to_author=author_details)
            friend_request_status = True
        except FriendRequest.DoesNotExist:
            friend_request_status = False
        friends_count = friends.count()
        posts = posts.order_by('-published')
        origin = 'host'
    except:
        remote_posts = get_stream(request)
        for authors in remote_posts[1]:
            if author_id == authors.id:
                author_details = authors

        for remote_post in remote_posts[0]:
            if remote_post.author == author_details:
                posts.append(remote_post)

    post_likes_dict = {}
    post_id_dict = {}
    shared_by = {}
    for post in posts:
        if origin == 'host':
            post_likes_dict[post] = post.likes.all().count()
            post_id_dict[post] = post.id
            shared_by[post] = request.user in post.shared_by.all()
        else:
            post_likes_dict[post] = -1
    return render(request, 'socialdist/author_profile.html', {'posts': post_likes_dict, 'author': author_details.username,
                                                              'author_id': author_id, 'friend_status': friend_status,
                                                              'friend_request_status': friend_request_status,
                                                              'friends_count': friends_count, 'post_id': post_id_dict,
                                                              'shared_by': shared_by, 'origin': origin})




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



@login_required
def user_settings(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ImageForm()
    return render(request, 'socialdist/user_settings.html', {'form': form})

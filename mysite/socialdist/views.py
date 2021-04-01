from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CreatePostForm, ImageForm, AuthorCreationForm, CreateCommentForm
from .models import *
from rest_framework import viewsets
from .serializers import *
from .views_helper import *
import requests
from rest_framework.parsers import JSONParser

# Create your views here.

def index(request):
    return render(request, "socialdist/index.html")


class SignUpView(generic.CreateView):
    form_class = AuthorCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def feed(request):
    # post_likes_dict - contains a count of likes on a post
    # post_id_dict - contains the id of the post to iterate through the dictionaries
    # post_liked - contains the boolean value of the current user's like on the post
    #can loop over nodes and add each to new_posts
    posts = get_foreign_posts('http://hermes-cmput404.herokuapp.com/api/') #this should not be hard coded, should be passing nodes
    posts_query = Post.objects.all().order_by('-created_at')
    for post in posts_query:
        posts.append(post)
    post_likes_dict = {}
    post_id_dict = {}
    post_liked = {}
    post_shared = {}
    for post in posts:
        print(post)
        post_likes_dict[post] = post.likes.all().count()
        post_liked[post] = request.user in post.likes.all()
        post_id_dict[post] = post.id
        post_shared[post] = request.user in post.shared_by.all()
    return render(request, 'socialdist/feed.html', {'posts': post_likes_dict, 'post_id': post_id_dict, 'post_liked': post_liked, 'post_shared': post_shared})


def image_view(request):
    # if request.method == 'POST':
    #     form = ImageForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('success')
    # else:
    #     form = ImageForm()
    # return render(request, 'socialdist/image_upload.html', {'form' : form})
    pass


def success(request):
    return HttpResponse('successfully uploaded')


def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        post = form.save(commit=False)
        post.created_by = request.user
        # Save post in database.
        post.save()
        # Rediect to post list.
        return redirect('feed')
    elif request.method == 'GET':
        # GET evaluated when form loaded.
        form = CreatePostForm()
        # Render the view with the form for the user to fill out.
        return render(request, 'socialdist/create_post.html', {'form': form})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    post.delete()
    posts = Post.objects.all().order_by('-created_at')
    post_likes_dict = {}
    post_id_dict = {}
    post_liked = {}
    for post in posts:
        post_likes_dict[post] = post.likes.all().count()
        post_liked[post] = request.user in post.likes.all()
        post_id_dict[post] = post.id
    return render(request, 'socialdist/feed.html', {'posts': post_likes_dict, 'post_id': post_id_dict, 'post_liked': post_liked})


def user_settings(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ImageForm()
    return render(request, 'socialdist/user_settings.html', {'form': form})

def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = post.likes.all()
    likes_count = likes.count()
    liked = request.user in likes
    shared = request.user in post.shared_by.all()
    comments = None
    try:
        comments = Comment.objects.filter(**{'post': post_id})
    except Comment.DoesNotExist:
        comments = None
    form = CreateCommentForm()

    if request.method == 'GET':
        return render(request, 'socialdist/view_post.html', {'post':post, 'post_id': post_id, 'likes_count': likes_count,'liked': liked, 'shared_post':shared, 'comments':comments, 'form':form})
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        form.save()
        return redirect(request.META['HTTP_REFERER'])



def author_profile(request, author_id):
    author_details = get_object_or_404(Author, id=author_id)
    posts = Post.objects.filter(**{'created_by': author_details}) | Post.objects.filter(**{'shared_by': author_details})
    following = author_details in request.user.following.all()
    friends = following and (author_details in request.user.followers.all())
    followers_count = author_details.followers.all().count()
    posts = posts.order_by('-created_at')
    post_likes_dict = {}
    post_id_dict = {}
    shared_by = {}
    for post in posts:
        post_likes_dict[post] = post.likes.all().count()
        post_id_dict[post] = post.id
        shared_by[post] = request.user in post.shared_by.all()
    return render(request, 'socialdist/author_profile.html', {'posts': post_likes_dict, 'author': author_details.username,
                                                              'author_id': author_id, 'following': following,
                                                              'friends': friends, 'followers_count': followers_count,
                                                              'post_id': post_id_dict, 'shared_by': shared_by})


def follow(request, author_id):
    from_author = request.user
    to_author = Author.objects.get(id=author_id)
    if (from_author not in to_author.followers.all()) and (to_author not in from_author.following.all()):
        from_author.following.add(to_author)
        to_author.followers.add(from_author)
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('already following')


def unfollow(request, author_id):
    from_author = request.user
    to_author = Author.objects.get(id=author_id)
    if (from_author in to_author.followers.all()) and (to_author in from_author.following.all()):
        from_author.following.remove(to_author)
        to_author.followers.remove(from_author)
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('not following')

def followers(request, author_id):
    author_details = Author.objects.get(id=author_id)
    followers_list = author_details.followers.all()
    author_name = author_details.username
    return render(request, 'socialdist/followers.html', {'author': author_name, 'followers': followers_list})

def like(request, post_id):
    the_post = Post.objects.get(id=post_id)
    from_author = request.user
    if request.user not in the_post.likes.all():
        the_post.likes.add(from_author)
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('already liked')

def unlike(request, post_id):
    the_post = Post.objects.get(id=post_id)
    from_author = request.user
    if request.user in the_post.likes.all():
        the_post.likes.remove(from_author)
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('not liked')

def share(request, post_id):
    the_post = Post.objects.get(id=post_id)
    from_author = request.user
    if request.user not in the_post.shared_by.all():
        the_post.shared_by.add(from_author)
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('already shared')

def unshare(request, post_id):
    the_post = Post.objects.get(id=post_id)
    from_author = request.user
    if request.user in the_post.shared_by.all():
        the_post.shared_by.remove(from_author)
        return redirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponse('not shared')

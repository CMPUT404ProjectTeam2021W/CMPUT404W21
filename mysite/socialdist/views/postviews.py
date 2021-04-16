from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from ..forms import CreatePostForm, ImageForm, AuthorCreationForm, CreateCommentForm
from ..models import *
from .views_helper import *
from .authenticationviews import *
from django.views.decorators.csrf import csrf_exempt




def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        post = form.save(commit=False)
        post.author = request.user
        if post.categories == 'image/jpeg' or post.categories == 'image/png':
            new_post_descript = image_as_post(post.description)
            if new_post_descript == 100:
                post.categories = 'text/plain'
                post.description = 'image size too large, please reduce size and try again' #can probably redirecthere or something better 
            elif new_post_descript == 110:
                post.categories = 'text/plain'
                post.description = 'Wrong format'
            else:                                                                          # maybe redirect with error message showing
                post.description = new_post_descript
            
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

def edit_post(request):
    if request.method == 'POST':
        print("yes were here")
        data = request.POST
        post_found = Post.objects.get(id=data['post_id'])
        post_found.title = data['title']
        print(data['title'])
        post_found.description = data['description']
        post_found.save()
        print("yesss")
        return HttpResponse('Profile Updated')
    else:
        print("noooo")
        return HttpResponse('Failure')


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('/feed')


def like(request, post_id):
    the_post = Post.objects.get(id=post_id)
    from_author = request.user
    try:
        Like.objects.get(author=from_author, object=the_post)
        return HttpResponse('already liked')
    except Like.DoesNotExist:
        like_obj = Like(author=from_author, object=the_post)
        like_obj.save()
        return redirect(request.META['HTTP_REFERER'])


def unlike(request, post_id):
    the_post = Post.objects.get(id=post_id)
    from_author = request.user
    try:
        like_obj = Like.objects.get(author=from_author, object=the_post)
        like_obj.delete()
        return redirect(request.META['HTTP_REFERER'])
    except Like.DoesNotExist:
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


def unlisted_posts(request):
        posts = Post.objects.filter(author=request.user).order_by('-published')
        posts = posts.filter(unlisted='True')
        post_likes_dict = {}
        post_id_dict = {}
        post_liked = {}
        post_shared = {}
        for post in posts:
            if post.origin == "https://hermes-cmput404.herokuapp.com/":
                post_likes_dict[post] = Like.objects.filter(**{'object': post}).count()
                try:
                    post_liked[post] = Like.objects.get(author=request.user, object=post)
                except Like.DoesNotExist:
                    post_liked[post] = False
                post_id_dict[post] = post.id
                post_shared[post] = request.user in post.shared_by.all()
            else:
                post_likes_dict[post] = -1
            post_id_dict[post] = post.id
        return render(request, 'socialdist/unlisted.html', {'posts': post_likes_dict, 'post_id': post_id_dict,
                                                            'post_liked': post_liked})


@login_required
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likes = Like.objects.filter(**{'object': post})
    likes_count = likes.count()

    shared = request.user in post.shared_by.all()
    comments = None
    try:

        comments = Comment.objects.filter(**{'post': post})
    except Comment.DoesNotExist:
        comments = None
    try:
        liked = Like.objects.get(author=request.user, object=post)
    except Like.DoesNotExist:
        liked = None
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



@login_required
def feed(request):
    # post_likes_dict - contains a count of likes on a post
    # post_id_dict - contains the id of the post to iterate through the dictionaries
    # post_liked - contains the boolean value of the current user's like on the post
    foreign_posts = get_stream(request) # get posts from other server

    full_posts = []

    local_posts = Post.objects.all().order_by("-published")

    local_posts = local_posts.filter(visibility='public')
    local_posts = local_posts.filter(unlisted='False')

    post_likes_dict = {}
    post_id_dict = {}
    post_liked = {}
    post_shared = {}
    friend_requests = list()
    for foreign_post in foreign_posts[0]:
        full_posts.append(foreign_post)

    full_posts += list(local_posts)
    full_posts.sort(key=lambda x: x.published, reverse=True)
    # print(full_posts)
    for post in full_posts:

        if post.origin == "https://hermes-cmput404.herokuapp.com/":
            post_likes_dict[post] = Like.objects.filter(**{'object': post}).count()
            try:
                post_liked[post] = Like.objects.get(author=request.user, object=post)
            except Like.DoesNotExist:
                post_liked[post] = False
            post_id_dict[post] = post.id
            post_shared[post] = request.user in post.shared_by.all()
        else:
            post_likes_dict[post] = -1

    try:
        friend_requests = FriendRequest.objects.filter(**{'to_author': request.user})
    except FriendRequest.DoesNotExist:
        friend_requests = list()


    return render(request, 'socialdist/feed.html', {'posts': post_likes_dict, 'post_id': post_id_dict,
                                                    'post_liked': post_liked, 'post_shared': post_shared,
                                                    'friend_requests': friend_requests})

@login_required
def friends_feed(request):
    # post_likes_dict - contains a count of likes on a post
    # post_id_dict - contains the id of the post to iterate through the dictionaries
    # post_liked - contains the boolean value of the current user's like on the post
    foreign_posts = get_stream(request) # get posts from other server

    full_posts = []

    friends = request.user.friends.all()

    local_posts = Post.objects.all().order_by("-published")

    local_posts = local_posts.filter(visibility='friends')
    local_posts = local_posts.filter(unlisted='False')

    post_likes_dict = {}
    post_id_dict = {}
    post_liked = {}
    post_shared = {}
    friend_requests = list()
    if len(foreign_posts) != 0:
        for foreign_post in foreign_posts[0]:
            if foreign_post.visibility == 'friends':
                full_posts.append(foreign_post)

    full_posts += list(local_posts)

    for post in full_posts:
        if post.author not in friends:
            full_posts.remove(post)

    full_posts.sort(key=lambda x: x.published, reverse=True)
    # print(full_posts)
    for post in full_posts:

        if post.origin == "https://hermes-cmput404.herokuapp.com/":
            post_likes_dict[post] = Like.objects.filter(**{'object': post}).count()
            try:
                post_liked[post] = Like.objects.get(author=request.user, object=post)
            except Like.DoesNotExist:
                post_liked[post] = False
            post_id_dict[post] = post.id
            post_shared[post] = request.user in post.shared_by.all()
        else:
            post_likes_dict[post] = -1

    try:
        friend_requests = FriendRequest.objects.filter(**{'to_author': request.user})
    except FriendRequest.DoesNotExist:
        friend_requests = list()


    return render(request, 'socialdist/feed.html', {'posts': post_likes_dict, 'post_id': post_id_dict,
                                                    'post_liked': post_liked, 'post_shared': post_shared,
                                                    'friend_requests': friend_requests})

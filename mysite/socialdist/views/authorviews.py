from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from ..forms import CreatePostForm, ImageForm, AuthorCreationForm, CreateCommentForm
from ..models import *


@login_required
def author_profile(request, author_id):
    author_details = get_object_or_404(Author, id=author_id)
    posts = Post.objects.filter(**{'author': author_details}) | Post.objects.filter(**{'shared_by': author_details})
    following = author_details in request.user.following.all()
    friends = following and (author_details in request.user.followers.all())
    followers_count = author_details.followers.all().count()
    posts = posts.order_by('-published')
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

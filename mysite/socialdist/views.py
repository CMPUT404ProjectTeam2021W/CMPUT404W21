from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import CreatePostForm, ImageForm, AuthorCreationForm
from .models import *


# Create your views here.

def index(request):
    return render(request, "socialdist/index.html")


class SignUpView(generic.CreateView):
    form_class = AuthorCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def feed(request):
    posts = Post.objects.all().order_by('-created_at')[:10]
    return render(request, 'socialdist/feed.html', {'posts': posts})


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
        # This branch runs when the user submits the form.
        # Create an instance of the form with the submitted data.
        form = CreatePostForm(request.POST)
        # Convert the form into a model instance.  commit=False postpones
        # saving to the database.
        post = form.save(commit=False)
        # Make the currently logged in user the Post creator.
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


def profile_posts(request):
    posts = Post.objects.filter(**{'created_by': request.user})
    # posts = Post.objects.all().filter('-created_by'=request.user)

    # posts = Post.objects.filter(created_by=request.user)
    return render(request, 'socialdist/profile.html', {'posts': posts})


def user_settings(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ImageForm()
    return render(request, 'socialdist/user_settings.html', {'form': form})


def author_profile(request, author_id):
    author_details = get_object_or_404(Author, id=author_id)
    posts = Post.objects.filter(**{'created_by': author_details})
    following = (request.user in author_details.followers.all()) and (author_details in request.user.following.all())
    followers_count = author_details.followers.all().count()
    return render(request, 'socialdist/author_profile.html', {'posts': posts, 'author': author_details.username,
                                                              'author_id': author_id, 'following': following,
                                                              'followers_count': followers_count})


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

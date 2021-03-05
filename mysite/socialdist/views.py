from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import User
from .forms import ImageForm, SignUpForm, PostTextForm


# Create your views here.

def index(request):
    return render(request, "socialdist/index.html")
def create_post(request):

    user = get_object_or_404(User)
    new_post = None
    if request.method == 'POST':
        post_form = PostTextForm(data=request.POST)
        new_post = post_form.save(commit=False)
        new_post.user = request.user.username
        new_post.save()
    else:
        post_form = PostTextForm()
    return render(request, "socialdist/test_post.html", {
        'user':user,
        'new_post':new_post,
        'post_form':post_form
    })

def feed(request):
    return render(request, "socialdist/feed.html")
class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

def image_view(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ImageForm()
    return render(request, 'socialdist/image_upload.html', {'form' : form})

def success(request):
    return HttpResponse('successfully uploaded')

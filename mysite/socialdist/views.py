from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import ImageForm, MyUserCreationForm


# Create your views here.

def index(request):
    return render(request, "socialdist/index.html")

def feed(request):
    return render(request, "socialdist/feed.html")
class SignUpView(generic.CreateView):
    form_class = MyUserCreationForm
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

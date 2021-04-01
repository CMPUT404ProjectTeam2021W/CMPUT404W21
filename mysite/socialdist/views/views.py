# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
# from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse_lazy
# from django.views import generic
# from .forms import CreatePostForm, ImageForm, AuthorCreationForm, CreateCommentForm
# from .models import *

from .postviews import *
from .authenticationviews import *
from .authorviews import *


# Create your views here.


# def image_view(request):
#     # if request.method == 'POST':
#     #     form = ImageForm(request.POST, request.FILES)
#     #     if form.is_valid():
#     #         form.save()
#     #         return redirect('success')
#     # else:
#     #     form = ImageForm()
#     # return render(request, 'socialdist/image_upload.html', {'form' : form})
#     pass
#
# def success(request):
#     return HttpResponse('successfully uploaded')

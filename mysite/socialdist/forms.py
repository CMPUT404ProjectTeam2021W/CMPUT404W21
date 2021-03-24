from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from .models import MyUser



class MyUserCreationForm(UserCreationForm):
    github_link = forms.URLField(required=False)

    class Meta:
        model = MyUser
        fields = ('username', 'github_link', )


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = MyUser
        fields = ('username', 'github_link')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['new_image']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['contents', 'access_level']

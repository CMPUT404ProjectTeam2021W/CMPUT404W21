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

    # class Meta:
    #     model = Post
    #     exclude = ('poster', 'created_on')
    #
    # def __init__(self, poster, *args, **kwargs):
    #     self.poster = poster
    #
    #     super(CreatePostForm, self).__init__(*args, **kwargs)
    #
    # def save(self):
    #     post = super(CreatePostForm, self).save(commit=False)
    #     post.poster = self.poster
    #     post.save(commit=True)
    #     return post
    class Meta:
        model = Post
        fields = ['contents', 'access_level']

class LikePostForm(forms.ModelForm):


    class Meta:
        model = LikeButton
        
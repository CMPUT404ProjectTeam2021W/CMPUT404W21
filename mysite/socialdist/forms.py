from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *



class AuthorCreationForm(UserCreationForm):
    github_link = forms.URLField(required=False)

    class Meta:
        model = Author
        fields = ('username', 'github_link', )


class AuthorChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = Author
        fields = ('username', 'github_link')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['new_image']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['contents', 'access_level']

class CreateCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=120)
    class Meta:
        model = Comment
        exclude = (
            'post',
            'author',
            'created_at'
        )

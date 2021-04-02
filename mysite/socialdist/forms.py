from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *



class AuthorCreationForm(UserCreationForm):
    github = forms.URLField(required=False)

    class Meta:
        model = Author
        fields = ('username', 'github', )
    def __init__(self, *args, **kwargs):
        super(AuthorCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None



class AuthorChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = Author
        fields = ('username', 'github')


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['new_image']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','description', 'visibility', 'unlisted', 'categories']
        exclude = ("origin",)

class CreateCommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=120)
    class Meta:
        model = Comment
        exclude = (
            'post',
            'author',
            'published'
        )

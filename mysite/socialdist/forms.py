from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    github_link = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ('username', 'github_link','password1', 'password2' )

    def save(self, commit=True):
        # user = super(SignUpForm, self).save(commit=False)
        author.user = super(SignUpForm, self).save(commit=False)
        author.github_link = self.cleaned_data['github_link']
        if commit:
            author.user.save()
        return author

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'new_image']

class PostTextForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea, max_length=2500, required=True)
    
    # class Meta:
    #     model = PostContentText
    #     fields = ('text','user')

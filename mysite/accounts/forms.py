from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    github_link = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ('username', 'github_link', 'password1', 'password2', )

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.github_link = self.cleaned_data['github_link']
        if commit:
            user.save()
        return user

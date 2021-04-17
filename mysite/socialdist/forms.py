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

#class GithubChangeForm(forms.ModelForm):
#    github = forms.URLField()
#
#    class Meta:
#        model = Author
#        fields = ('github', )
#    
#    def save(self, user_id):
#        author = uthor.objects.get(id=user_id)
#
#        author.github = self.cleaned_data.get('github')
#        author.save()
#
#        return author

class SettingChangeForm(forms.ModelForm):
    github = forms.URLField(label="New Github URL", required=False)
    password = forms.CharField(label="Old Password", widget=forms.PasswordInput, required=False)
    new_password1 = forms.CharField(label="New Password", widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label="New Password confirmation", widget=forms.PasswordInput, required=False)

    class Meta:
        model = Author
        fields = ('github', 'password')

    def check_github(self):
        github = self.cleaned_data.get('github')

        if github == '':
            return False
        
        return True

    def clean_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "The two new password fields didn't match.",
                code='password_mismatch',
            )

        return password2

    def save(self, user_id):
        try:
            author = Author.objects.get(id=user_id)
            modified = False
        except Author.DoesNotExist:
            return False
        
        passowrd_valid = author.check_password(self.cleaned_data.get("password"))
        if passowrd_valid:
            modified == True
            new_password = self.clean_password2()
            author.set_password(new_password)

        valid_github = self.check_github()
        if valid_github:
            modified = True
            github = self.cleaned_data.get('github')
            author.github = github

        if modified:
            author.save()
        
        return author

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

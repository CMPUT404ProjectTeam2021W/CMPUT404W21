from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
import uuid
from markdownx.models import MarkdownxField

# Create your models here.
class Author(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.CharField(max_length=200, null=True, blank=True)
    github = models.URLField(default='', blank=True)
    image = models.ImageField(default='../img/face.svg', upload_to='images/')
    friends = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="friends+")
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        self.url = '{}/author/{}'.format('http://hermes-cmput404.herokuapp.com', self.id)
        super(Author, self).save(*args, **kwargs)

class Post(models.Model):
        ACCESS_PUBLIC = 'public'
        ACCESS_PRIVATE = 'private'
        ACCESS_FRIENDS = 'friends'
        CATEGORY_PLAIN = 'text/plain'
        CATEGORY_IMAGE_PNG = 'image/png'
        CATEGORY_IMAGE_JPEG = 'image/jpeg'
        CATEGORY_MARKDOWN = 'text/markdown'
        visibility_choices = [
            (ACCESS_PUBLIC, 'Public'),
            (ACCESS_PRIVATE, 'Private'),
            (ACCESS_FRIENDS, 'Friends Only'),
        ]
        categories_choices = [
        (CATEGORY_PLAIN, 'text/plain'),
        (CATEGORY_IMAGE_PNG, 'image/png'),
        (CATEGORY_IMAGE_JPEG, 'image/jpeg'),
        (CATEGORY_MARKDOWN, 'text/markdown')
        ]
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        # description = models.CharField(widgets=forms.Textarea, max_length=140, null=True, blank=True)
        title = models.CharField(max_length=140, null=True, blank=True)
        description = MarkdownxField() #models.TextField(max_length=140, null=True, blank=True)
        visibility = models.CharField(max_length=140, choices=visibility_choices, default=ACCESS_PUBLIC)
        unlisted = models.BooleanField(default=False)
        author = models.ForeignKey(Author, on_delete=models.CASCADE)
        published = models.DateTimeField(auto_now_add=True)
        categories = models.CharField(max_length=140, choices=categories_choices, default=CATEGORY_PLAIN)
        origin = models.CharField(max_length=200, default="https://hermes-cmput404.herokuapp.com/")
        shared_by = models.ManyToManyField(Author, symmetrical=False, blank=True, related_name="shared")

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    post = models.ForeignKey(Post, related_name='CommentPost', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, related_name='authorComment', on_delete=models.CASCADE)
    comment = models.TextField(default="")
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {}".format(self.author, self.published, self.id)

    def __repr__(self):
        return "{} - {} - {} ".format(self.author, self.published, self.id)

class Image(models.Model):
    username = models.CharField(max_length=50)
    new_image = models.ImageField(upload_to='images/')

class Server(models.Model):
    id = models.AutoField(primary_key=True, editable=False, blank=False)
    hostname = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=200, null=True, blank=True)

class FriendRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    from_author = models.ForeignKey(Author, related_name='from_author', on_delete=models.CASCADE)
    to_author = models.ForeignKey(Author, related_name='to_author', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    author = models.ForeignKey(Author, related_name='liked_author', on_delete=models.CASCADE)
    object = models.ForeignKey(Post, related_name='liked_object', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

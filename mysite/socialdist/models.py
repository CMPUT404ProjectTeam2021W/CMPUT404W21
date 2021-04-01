from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
import uuid

# Create your models here.
class Author(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    url = models.CharField(max_length=200, null=True, blank=True)
    github_link = models.URLField(default='')
    friends = models.TextField(default='')
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers+")
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="following+")

    def save(self, *args, **kwargs):

        self.url = '{}/author/{}'.format('localhost:8000', self.id)
        super(Author, self).save(*args, **kwargs)

class Post(models.Model):
        ACCESS_PUBLIC = 'public'
        ACCESS_PRIVATE = 'private'
        ACCESS_FRIENDS = 'friends'
        ACCESS_LEVEL_CHOICES = [
            (ACCESS_PUBLIC, 'Public'),
            (ACCESS_PRIVATE, 'Private'),
            (ACCESS_FRIENDS, 'Friends Only'),
        ]
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        # contents = models.CharField(widgets=forms.Textarea, max_length=140, null=True, blank=True)
        title = models.CharField(max_length=140, null=True, blank=True)
        contents = models.TextField(max_length=140, null=True, blank=True)
        access_level = models.CharField(max_length=140, choices=ACCESS_LEVEL_CHOICES, default=ACCESS_PUBLIC)
        unlisted = models.BooleanField(default=False)
        created_by = models.ForeignKey(Author, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)
        likes = models.ManyToManyField(Author, symmetrical=False, blank=True, related_name="posts+")
        shared_by = models.ManyToManyField(Author, symmetrical=False, blank=True, related_name="shared")

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=False)
    post = models.ForeignKey(Post, related_name='CommentPost', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, related_name='authorComment', on_delete=models.CASCADE)
    comment = models.TextField(default="")
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {}".format(self.author, self.created_at, self.id)

    def __repr__(self):
        return "{} - {} - {} ".format(self.author, self.created_at, self.id)

class Image(models.Model):
    username = models.CharField(max_length=50)
    new_image = models.ImageField(upload_to='images/')

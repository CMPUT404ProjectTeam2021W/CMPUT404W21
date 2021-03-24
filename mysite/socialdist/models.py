from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

# Create your models here.
class MyUser(AbstractUser):
    github_link = models.URLField(default='')
    friends = models.TextField(default='')

class Post(models.Model):
        # title = models.CharField(max_length=50)
        # poster = models.ForeignKey(MyUser, on_delete=models.CASCADE)
        # body = models.CharField(max_length=2500, blank="False")
        # created_on = models.DateTimeField(auto_now=True)
        ACCESS_PUBLIC = 0
        ACCESS_PRIVATE = 1
        ACCESS_LEVEL_CHOICES = [
            (ACCESS_PUBLIC, 'Public'),
            (ACCESS_PRIVATE, 'Private'),
        ]

        # contents = models.CharField(widgets=forms.Textarea, max_length=140, null=True, blank=True)
        contents = models.TextField(max_length=140, null=True, blank=True)
        access_level = models.IntegerField(choices=ACCESS_LEVEL_CHOICES, default=ACCESS_PUBLIC)

        created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE)
        created_at = models.DateTimeField(auto_now_add=True)

class Image(models.Model):
    username = models.CharField(max_length=50)
    new_image = models.ImageField(upload_to='images/')

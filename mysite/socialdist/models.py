from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class MyUser(AbstractUser):
    github_link = models.URLField(default='')
    friends = models.TextField(default='')


class Post(models.Model):

    title = models.CharField(max_length=50)
    poster = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    body = models.CharField(max_length=2500, blank="False")
    created_on = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.CharField(max_length=2500)
    commentor = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Image(models.Model):
    username = models.CharField(max_length=50)
    new_image = models.ImageField(upload_to='images/') 

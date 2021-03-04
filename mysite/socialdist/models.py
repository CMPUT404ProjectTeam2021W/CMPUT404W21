from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

class Author(models.Model):
    githublink = models.URLField()
    username = models.CharField(max_length=20)

class Image(models.Model):
    name = models.CharField(max_length=50)
    new_image = models.ImageField(upload_to='images/') 

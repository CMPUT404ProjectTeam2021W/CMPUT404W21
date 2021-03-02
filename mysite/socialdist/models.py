from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)

class Author(models.Model):
    githublink = models.URLField()
    username = models.CharField(max_length=20)
    
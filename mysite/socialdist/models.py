from django.db import models
from django.contrib.auth.models import User

#class User(models.Model):
#    name = models.CharField(max_length=200)

class Author(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    githublink = models.URLField()
    name = models.CharField(max_length=20)

    def __str__(self):
        if user:
            return "{}".format(str(user.username))

# # Create your models here.
# class User(User):
#     name = User.username
#     password = User.password
#
#     class Meta:
#         constraints = [
#             models.CheckConstraint(
#                 name='username_password_is_different',
#                 check=models.Q(password=models.F('username')),
#             )
#         ]

class Post(models.Model):
    CONTENT_TYPE = (
        ('T', 'Text'),
        ('I', 'Image'),
        ('L', 'ImageLink'),
        ('C', 'CommonMark'),
    )

    title = models.CharField(max_length=50)
    contenttype = models.CharField(max_length=1, choices=CONTENT_TYPE, default='T')
    poster = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)



class PostContentText(models.Model):
    text = models.CharField(max_length=2500, blank="False")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class PostCotentImageLink(models.Model):
    text = models.URLField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    comment = models.CharField(max_length=2500)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Image(models.Model):
    name = models.CharField(max_length=50)
    new_image = models.ImageField(upload_to='images/')

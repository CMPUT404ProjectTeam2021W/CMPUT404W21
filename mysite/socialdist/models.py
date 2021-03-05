from django.db import models

#class User(models.Model):
#    name = models.CharField(max_length=200)

class Author(models.Model):
    githublink = models.URLField()
    name = models.CharField(max_length=20)
    
# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200, default="")

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='username_password_is_different',
                check=models.Q(password=models.F('username')),
            )
        ]

class Post(models.Model):
    CONTENT_TYPE = (
        ('T', 'Text'),
        ('I', 'Image'),
        ('L', 'ImageLink'),
        ('C', 'CommonMark'),
    )

    title = models.CharField(max_length=50)
    contenttype = models.CharField(max_length=1, choices=CONTENT_TYPE, default='T')
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)

    

class PostContentText(models.Model):
    text = models.CharField(max_length=2500)
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

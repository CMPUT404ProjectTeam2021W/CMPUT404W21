from django.db import models

#class User(models.Model):
#    name = models.CharField(max_length=200)

#class Author(models.Model):
#    githublink = models.URLField()
#    username = models.CharField(max_length=20)
    
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='username_password_is_different',
                check=models.Q(password=models.F(username)),
            )
        ]

class Post(models.Model):
    title = models.CharField(max_length=50)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta: 
        abstract = True

class TextPost(Post):
    content = models.CharField(max_length=2500)

    class Meta(Post.Meta):
        db_table = 'text_post'

class Comment(models.Model):
    comment = models.CharField(max_length=2500)
    commentor = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


from django.test import TestCase, Client

# Create your tests here.
from django.test import TestCase
from .models import Author, Post, Comment

# Create your tests here.

class AuthorTestCase(TestCase):

    def test_author_creation(self):
        new_id = 1
        new_url = '{}/author/{}'.format('localhost:8000', new_id)
        new_github_link = 'https://github.com/BigDawn01'
        author = Author(id=new_id, url=new_url, github_link=new_github_link)
        author.save()

        current_author = Author.objects.get(id=new_id)
        self.assertEqual(current_author.url, new_url)

    def test_post_creation(self):
        new_id = 1
        new_url = '{}/author/{}'.format('localhost:8000', new_id)
        new_github_link = 'https://github.com/BigDawn01'
        author = Author(id=new_id, url=new_url, github_link=new_github_link)
        author.save()

        new_id = 1
        new_title = "First Post"
        new_description = "This is just a description"
        first_author = Author.objects.get(id=new_id)
        post = Post(id=new_id, title=new_title, description=new_description, author=first_author)
        post.save()

        new_post = Post.objects.get(id=new_id)
        self.assertEqual(new_post.title, new_title)
        self.assertEqual(new_post.description, new_description)
        self.assertEqual(new_post.author.url, new_url)
        self.assertEqual(new_post.author.github_link, new_github_link)
    
    def test_comment_creation(self):
        new_id = 1
        new_url = '{}/author/{}'.format('localhost:8000', new_id)
        new_github_link = 'https://github.com/BigDawn01'
        author = Author(id=new_id, url=new_url, github_link=new_github_link)
        author.save()

        new_title = "First Post"
        new_description = "This is just a description"
        first_author = Author.objects.get(id=new_id)
        post = Post(id=new_id, title=new_title, description=new_description, author=first_author)
        post.save()

        comment = Comment(id=new_id, post=post, author=author, comment="This is the comment")
        comment.save()

        first_commment = Comment.objects.get(id=new_id)

        self.assertEqual(first_commment.comment, "This is the comment")
        self.assertEqual(first_commment.author.url, new_url)
        self.assertEqual(first_commment.author.github_link, new_github_link)
        self.assertEqual(first_commment.post.description, new_description)
        self.assertEqual(first_commment.__str__(), "{} - {} - {}".format(first_commment.author, first_commment.published, first_commment.id))
        self.assertEqual(first_commment.__repr__(), "{} - {} - {} ".format(first_commment.author, first_commment.published, first_commment.id))

    #def test_get_html(self):

        #new_id = 1
        #new_url = '{}/author/{}'.format('localhost:8000', new_id)
        #new_github_link = 'https://github.com/BigDawn01'
        #author = Author(id=new_id, url=new_url, github_link=new_github_link)
        #author.save()
        #current_author = Author.objects.get(id=new_id)

        #c = Client()

        #response = c.get('/login/')
        #print(response.status_code)
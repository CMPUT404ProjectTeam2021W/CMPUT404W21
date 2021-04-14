from django.test import TestCase, Client

# Create your tests here.
from django.test import TestCase
from .models import Author, Post, Comment

# Create your tests here.

class ModelTestCase(TestCase):

    def test_author_creation(self):
        new_username = "Test123"
        new_password = "ThisISpass1234"
        new_github = 'https://www.github.com/BigDawn01'
        author = Author(username=new_username, github=new_github)
        author.set_password(new_password)
        author.save()

        current_author = Author.objects.get(username=author.username)
        self.assertEqual(current_author.id, author.id)
        self.assertEqual(current_author.username, new_username)
        self.assertEqual(current_author.github, new_github)
        self.assertEqual(current_author.url, author.url)
        self.assertEqual(True, author.check_password(new_password))

        new_password2 = "ThisISpass12345"
        new_github2 = 'https://www.github.com/BigDawn02'
        current_author.github = new_github2
        current_author.set_password(new_password2)
        current_author.save()

        current_author = Author.objects.get(username=author.username)
        self.assertEqual(current_author.id, author.id)
        self.assertEqual(current_author.username, new_username)
        self.assertEqual(current_author.github, new_github2)
        self.assertEqual(current_author.url, author.url)
        self.assertEqual(True, current_author.check_password(new_password2))


    def test_post_creation(self):
        new_username = "Test123"
        new_password = "ThisISpass1234"
        new_github = 'https://www.github.com/BigDawn01'
        author = Author(username=new_username, github=new_github)
        author.set_password(new_password)
        author.save()

        new_id = 1
        new_title = "First Post"
        new_description = "This is just a description"
        first_author = Author.objects.get(username=new_username)
        post = Post(id=1, title=new_title, description=new_description, author=first_author, visibility='public', unlisted=False)
        post.save()

        new_post = Post.objects.get(id=new_id)
        self.assertEqual(new_post.title, new_title)
        self.assertEqual(new_post.description, new_description)
        self.assertEqual(new_post.author.username, author.username)
        self.assertEqual(new_post.author.url, author.url)
        self.assertEqual(new_post.author.github, new_github)
        self.assertTrue(new_post.published)
        self.assertEqual(new_post.visibility, 'public')
        self.assertEqual(new_post.unlisted, False)

    def test_comment_creation(self):
        new_username = "Test123"
        new_password = "ThisISpass1234"
        new_github = 'https://www.github.com/BigDawn01'
        author = Author(username=new_username, github=new_github)
        author.set_password(new_password)
        author.save()

        new_id = 1
        new_title = "First Post"
        new_description = "This is just a description"
        first_author = Author.objects.get(username=new_username)
        post = Post(id=1, title=new_title, description=new_description, author=first_author, visibility='public', unlisted=False)
        post.save()

        comment = Comment(id=new_id, post=post, author=author, comment="This is the comment")
        comment.save()

        first_commment = Comment.objects.get(id=new_id)

        self.assertEqual(first_commment.comment, "This is the comment")
        self.assertEqual(first_commment.author.username, author.username)
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

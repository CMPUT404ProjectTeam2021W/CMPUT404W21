from django.test import TestCase, Client

# Create your tests here.
from django.test import TestCase
from .models import Author, Post, Comment, Server, FriendRequest, Like
from .forms import AuthorCreationForm
from django.urls import reverse
import uuid

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

        username1 = "Many1"
        password1 = "ThisISpass1234"
        github1 = 'https://www.github.com/many01'
        author1 = Author(username=username1, github=github1)
        author1.set_password(password1)
        author1.save()

        username2 = "Many2"
        password2 = "ThisISpass1234"
        github2 = 'https://www.github.com/many02'
        author2 = Author(username=username2, github=github2)
        author2.set_password(password2)
        author2.save()

        new_id = 1
        new_title = "First Post"
        new_description = "This is just a description"
        first_author = Author.objects.get(username=new_username)
        post = Post(id=1, title=new_title, description=new_description, author=first_author, visibility='public', unlisted=False)
        post.shared_by.add(author1)
        post.shared_by.add(author2)
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

    def test_server(self):
        hostname = "www.anotherhost.com"
        username = "Test123"
        password = "ThisISpass1234"
        server = Server(hostname=hostname, username=username, password=password)
        server.save()

        new_server = Server.objects.get(hostname=hostname, username=username)
        self.assertEqual(new_server.hostname, hostname)
        self.assertEqual(new_server.username, username)
        self.assertEqual(new_server.password, password)

    def test_friendrequest(self):
        username1 = "Test123"
        password1 = "ThisISpass1234"
        github1 = 'https://www.github.com/BigDawn01'
        author1 = Author(username=username1, github=github1)
        author1.set_password(password1)
        author1.save()

        username2 = "Test12345"
        password2 = "ThisISpass1234"
        github2 = 'https://www.github.com/BigDawn02'
        author2 = Author(username=username2, github=github2)
        author2.set_password(password2)
        author2.save()

        request_id = 1
        friend_request = FriendRequest(id=request_id, from_author=author1, to_author=author2)
        friend_request.save()

        new_friend_request = FriendRequest.objects.get(id=request_id)
        self.assertEqual(new_friend_request.from_author.username, username1)
        self.assertEqual(new_friend_request.to_author.username, username2)

    def test_like(self):
        username1 = "Test123"
        password1 = "ThisISpass1234"
        github1 = 'https://www.github.com/BigDawn01'
        author1 = Author(username=username1, github=github1)
        author1.set_password(password1)
        author1.save()        

        new_id = 1
        new_title = "First Post"
        new_description = "This is just a description"
        first_author = Author.objects.get(username=username1)
        post = Post(id=1, title=new_title, description=new_description, author=first_author, visibility='public', unlisted=False)
        post.save()

        like_id = 1
        like = Like(id=new_id, author=author1, object=post)
        like.save()

        new_like = Like.objects.get(id=like_id)
        self.assertEqual(new_like.author.username, username1)
        self.assertEqual(new_like.object.title, new_title)
        self.assertEqual(new_like.object.description, new_description)

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

class LoginTestCase(TestCase):

    def setUp(self) -> None:
        self.username = 'test'
        self.github = 'Http://www.github.com/test'
        self.password = 'Password12345'

    def test_index_page_url(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='socialdist/index.html')

    def test_signup_page_url(self):
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_signup_page_view_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_login_page_url(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/login.html')

class ViewTestCase(TestCase):

    def setUp(self) -> None:
        self.username = 'test'
        self.github = 'Http://www.github.com/test'
        self.password = 'Password12345'

        self.author = Author.objects.create(username=self.username, github=self.github)
        self.author.set_password(self.password)
        self.author.save()
        self.client.login(username=self.username, password=self.password)

        self.author2 = Author.objects.create(username='test2', github='Http://www.github.com/test2')
        self.author2.set_password(self.password)
        self.author2.save()

        self.post = Post.objects.create(id="06335e84-2872-4914-8c5d-3ed07d2a2f16", title="Test Post", description="This is a description", author=self.author)
        self.post.save()

    def test_feed(self):
        response = self.client.get('/feed/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='socialdist/feed.html')

    def test_user_settings(self):
        response = self.client.get('/user_settings/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='socialdist/user_settings.html')

    def test_author_profile(self):
        url = "/author/" + str(self.author.id) + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='socialdist/author_profile.html')

    def test_other_author_profile(self):
        url = "/author/" + str(self.author2.id) + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='socialdist/author_profile.html')

    def test_author_friend(self):
        url = "/author/" + str(self.author.id) + "/friends/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='socialdist/friends.html')

    def test_author_friend(self):
        url = "/create_post/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='socialdist/create_post.html')

    def test_author_friend_feed(self):
        url = "/friends_feed/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='socialdist/feed.html')

    def test_author_unlisted(self):
        url = "/unlisted/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='socialdist/unlisted.html')

    def test_view_post(self):
        url = "/posts/06335e84-2872-4914-8c5d-3ed07d2a2f16/view_post/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='socialdist/view_post.html')

    #def test_signup(self):
    #    response = self.client.post(reverse('signup'), 
    #    data={
    #        'username': self.username,
    #        'github': self.github,
    #        'password1': self.password,
    #        'password2': self.password,
    #    })
    #    self.assertEqual(response.status_code, 200)
        
        #authors = Author.objects.all()
        #self.assertEqual(authors.count(), 1)

    #def test_login(self):
    #    author = Author.objects.create(username=self.username, github=self.github)
    #    author.set_password(self.password)
    #    author.save()

        #login = self.client.login(username=self.username, password=self.password)
        #self.assertEqual(login, True)

    #def test_login_signup(self):

#        response = self.client.get('/')
#        self.assertEqual(response.status_code, 200)

#        response = self.client.get('/signup/')
#        self.assertEqual(response.status_code, 200)

#        response = self.client.post('/signup/', {'username': 'test', 'password': 'Super123456', 'github':'Http://www.github.com/test'})
#        self.assertEqual(response.status_code, 200)
#        print(response.content)

        #response = self.client.get('/signup/')
        #self.assertEqual(response.status_code, 200)

        #response = self.client.post('/signup/', {'username': 'test', 'password': 'Super123456', 'github':'Http://www.github.com/test'})
        #self.assertEqual(response.status_code, 200)

        #response = self.client.get('/login/')
        #self.assertEqual(response.status_code, 200)

        #response = self.client.post('/login/', {'username': 'test', 'password': 'Super123456'})
        #self.assertEqual(response.status_code, 200)

        #response = self.client.get('/feed/')
        #self.assertEqual(response.status_code, 200)

    #def test_setting(self):
        
    #    author = Author()
    #    author.username = 'test'
    #    author.github = 'Http://www.github.com/test'
    #    author.set_password('Super123456')

#class FormTestCase(TestCase):
#    def test_author_creation_github(self):
#        form = AuthorCreationForm(data={"username": "Test123456", "github": "123", "password": "Super123456"})
#        self.assertEqual(
#            form.errors["github"], ["Enter a valid URL."]
#        )
#    def test_author_creation_github(self):
#        form = AuthorCreationForm(data={"username": "Test123456", "github": "123", "password": "Test123456"})
#        print(form.errors["password"])
#        self.assertEqual(
#            form.errors["password"], ["password"]
#        )
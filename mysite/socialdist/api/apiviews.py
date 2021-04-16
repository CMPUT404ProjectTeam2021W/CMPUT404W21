import json

from requests.auth import HTTPBasicAuth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from ..models import *
from ..serializers import *
from ..pagination import *
from django.db.models import CharField, Value


class AuthorList(APIView):  # need to add POST: update profile
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        authors = Author.objects.all()
        data = AuthorSerializer(authors, many=True).data
        return Response(data)


class PostList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        posts = Post.objects.all()
        paginator = CustomPagination()  # PageNumberPagination()
        paged_results = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paged_results, many=True)

        next_page = paginator.get_next_link()
        if next_page == None:
            next_page = ""

        previous_page = paginator.get_previous_link()

        if previous_page == None:
            previous_page = ""

        result = {'count': paginator.page.paginator.count,
                  'next': next_page,
                  'previous': previous_page,
                  'posts': serializer.data
                  }

        return Response(data=result)

    def post(self, request):
        author = request.user
        data = request.POST

        description = data.get('description')
        title = data.get('title')
        visibility = data.get('visibility')
        unlisted = data.get('unlisted')
        categories = data.get('categories')
        origin = data.get('origin')
        response = dict()
        if description and title and unlisted and visibility and categories:
            if unlisted == 'false':
                unlisted = False
            else:
                unlisted = True
            if origin:
                post = Post.objects.create(
                    author=author, title=title, description=description,
                    visibility=visibility, categories=categories,
                    unlisted=unlisted, origin=origin)

                if post:
                    response['type'] = 'addedPost'
                    response['success'] = True
                    response['message'] = 'Post added'
                    return Response(response, status=200)
                else:
                    response['type'] = 'addedPost'
                    response['success'] = False
                    response['message'] = 'Failed to add post to server'
                    return Response(response, status=500)

            else:
                post = Post.objects.create(
                    author=author, title=title, description=description, visibility=visibility,
                    categories=categories, unlisted=unlisted)
                if post:
                    response['type'] = 'addedPost'
                    response['success'] = True
                    response['message'] = 'Post added'
                    return Response(response, status=200)
                else:
                    response['type'] = 'addedPost'
                    response['success'] = True
                    response['message'] = 'Failed to add post to server'
                    return Response(response, status=500)

        else:

            response['type'] = 'addedPost'
            response['success'] = False
            response['message'] = 'Missing fields'


class PostDetails(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, post_id, author_id):
        posts = Post.objects.get(id=post_id)
        data = dict()
        data['type'] = 'post'
        data['items'] = PostSerializer(posts, many=False).data
        # data = PostSerializer(posts, many=True, context={'request' : request}).data
        return Response(data=data)

    def put(self, request, post_id):
        response = dict()
        response['type'] = 'updatePost'

        try:
            post = Post.objects.get(id=post_id)
            current_user = request.user
            if current_user != post.author:
                response['success'] = False
                response['message'] = "Unauthorized:Not the original post owner"
                return Response(response, status=400)
            else:
                description = data.get('description')
                title = data.get('title')
                visibility = data.get('visibility')
                unlisted = data.get('unlisted')
                categories = data.get('categories')

                if description and title and unlisted and visibility and categories:
                    if unlisted == 'false':
                        unlisted = False
                    else:
                        unlisted = True
                post.description = description
                post.published = datetime.datetime.now()
                post.title = title
                post.categories = categories
                post.visibility = visibility
                post.unlisted = unlisted
                post.save()

                response['type'] = 'updatePost'
                response['success'] = True
                response['message'] = 'Post updated'
                return Response(response, status=200)

        except:

            response['type'] = 'updatePost'
            response['success'] = False
            response['message'] = 'Failed to update post to server'
            return Response(response, status=500)


class AuthorDetails(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        data = AuthorSerializer(author_obj).data
        return Response(data=data)


class FollowerList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        followers = author_obj.friends.all()
        data = dict()
        data['type'] = 'followers'
        data['items'] = AuthorSerializer(followers, many=True).data
        return Response(data=data)


class FollowerAction(APIView):  # NEED PUT: Add a follower (must be authenticated)
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id, foreign_author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        if author_obj.friends.filter(id=foreign_author_id).exists():
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, foreign_author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        if Author.objects.filter(id=foreign_author_id).exists():
            foreign_author_obj = Author.objects.get(id=foreign_author_id)
        else:
            hostname = "https://chatbyte.herokuapp.com/"
            url = hostname + "author/" + foreign_author_id + "/"
            headers = {'Origin': hostname, 'X-Request-User': url}
            response = request.get(url, headers=headers, auth=HTTPBasicAuth("chatbyte", "jeremychoo"))
            foreign_author_json = response.json()
            get_index = foreign_author_json["id"].find('author/')
            foreign_author_id = foreign_author_json["id"][get_index + len('author/'):]
            foreign_author_obj = Author.objects.create(id=foreign_author_id,
                                                       username=foreign_author_json['displayName'],
                                                       url=foreign_author_json['url'],
                                                       github=foreign_author_json['github'])
        author_obj.friends.add(foreign_author_obj)
        return Response(status.HTTP_200_OK)

    def delete(self, request, author_id, foreign_author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        if author_obj.friends.filter(id=foreign_author_id).exists():
            author_obj.friends.remove(Author.objects.get(id=foreign_author_id))
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentsList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id, post_id):
        post_obj = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post_obj).all()
        paginator = CustomPagination()  # PageNumberPagination()
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(result_page, many=True)

        next_page = paginator.get_next_link()
        if next_page == None:
            next_page = ""

        previous_page = paginator.get_previous_link()

        if previous_page == None:
            previous_page = ""



        result = {'count': paginator.page.paginator.count,
                  'next': next_page,
                  'previous': previous_page,
                  'comments': serializer.data
                  }

        return Response(data=result)

    def post(self, request, author_id, post_id):
        post_obj = get_object_or_404(Post, id=post_id)
        data = request.POST

        author = request.user
        comment = data.get('comment')
        published = data.get('published')
        id = data.get('id')
        response = dict()
        if author and comment and published and id:
            comment = Comment.object.create(id=id, post=post_obj, author=author, comment=comment, published=published)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class InboxAction(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        public_posts = Post.objects.filter(visibility='public', unlisted='False').all()
        friends_posts = Post.objects.filter(visibility='friends', unlisted='False').all()
        for post in friends_posts:
            if post.author not in author_obj.friends.all():
                friends_posts.remove(post)
        all_posts = (public_posts | friends_posts).order_by("-published")
        data = dict()
        data['type'] = 'inbox'
        data['author'] = author_obj.url
        data['items'] = PostSerializer(all_posts, many=True).data
        return Response(data=data)

    def post(self, request, author_id):
        data = request.POST
        if data.get('type') == "Like":
            get_index = data.get('author')['id'].find('author/')
            like_author_id = data.get('author')['id'][get_index + len('author/'):]
            author_obj = Author.objects.get_or_create(id=like_author_id,
                                                      username=data.get('author')['displayName'],
                                                      url=data.get('author')['url'],
                                                      github=data.get('author')['github'])
            get_index = data.get('object').find('posts/')
            post_id = data.get('object')[get_index + len('posts/'):]
            post_obj = Post.objects.get(id=post_id)
            like_obj = Like.object.create(author=author_obj, object=post_obj)
            return Response(status=status.HTTP_200_OK)
        if data.get('type') == "Follow":
            from_author = data.get('actor')
            to_author = data.get('object')
            get_index = from_author['id'].find('author/')
            from_author_id = from_author['id'][get_index + len('author/'):]
            get_index = to_author['id'].find('author/')
            to_author_id = to_author['id'][get_index + len('author/'):]
            from_author_obj = Author.objects.get_or_create(id=from_author_id, username=from_author['displayName'],
                                                           url=from_author['url'], github=from_author['github'])
            to_author_obj = Author.objects.get_or_create(id=to_author_id, username=to_author['displayName'],
                                                         url=to_author['url'], github=to_author['github'])
            friend_request = FriendRequest.objects.get_or_create(from_author=from_author_obj,
                                                                 to_author=to_author_obj)
            return Response(status=status.HTTP_200_OK)


class LikesList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id, post_id):
        post_obj = get_object_or_404(Post, id=post_id)
        like_obj_list = Like.objects.filter(object=post_obj).all()
        serializer = LikeSerializer(like_obj_list, many=True)
        data = dict()
        data["type"] = "likes"
        data["items"] = serializer.data
        return Response(data=data)


class LikedList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        like_obj_list = Like.objects.filter(author=author_obj).all()
        serializer = LikeSerializer(like_obj_list, many=True)
        data = dict()
        data["type"] = "liked"
        data["items"] = serializer.data
        return Response(data=data)

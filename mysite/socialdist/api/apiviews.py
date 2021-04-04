from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import get_object_or_404
from ..models import *
from ..serializers import *
from django.db.models import CharField, Value

class AuthorList(APIView):
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
        data = dict()
        data['type'] = 'post'
        data['items'] = PostSerializer(posts, many=True).data
        # data = PostSerializer(posts, many=True, context={'request' : request}).data
        return Response(data=data)
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
                    return Response(response, status = 200)
                else:
                    response['type'] = 'addedPost'
                    response['success'] = False
                    response['message'] = 'Failed to add post to server'
                    return Response(response, status = 500)

            else:
                post = Post.objects.create(
                author=author, title=title, description=description, visibility=visibility,
                categories=categories, unlisted=unlisted)
                if post:
                    response['type'] = 'addedPost'
                    response['success'] = True
                    response['message'] = 'Post added'
                    return Response(response, status = 200)
                else:
                    response['type'] = 'addedPost'
                    response['success'] = True
                    response['message'] = 'Failed to add post to server'
                    return Response(response, status = 500)

        else:

            response['type'] = 'addedPost'
            response['success'] = False
            response['message'] = 'Missing fields'



class PostDetails(APIView):
        authentication_classes = (SessionAuthentication, BasicAuthentication)
        permission_classes = (IsAuthenticated, IsAdminUser)
        def get(self, request, post_id):
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
                if current_user!= post.author:
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
                    return Response(response, status = 200)

            except:

                response['type'] = 'updatePost'
                response['success'] = False
                response['message'] = 'Failed to update post to server'
                return Response(response, status = 500)





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

class FollowerAction(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id, foreign_author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        data = dict()
        if author_obj.friends.filter(id=foreign_author_id).exists():
            data['detail'] = 'true'
        else:
            data['detail'] = 'false'
        return Response(data=data)

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
        serializer = CommentSerializer(comments, many=True)
        data = dict()
        data['type'] = "comments"
        data['items'] = serializer
        return Response(data=data)

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




''' class LikedList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        data = dict()
        posts = author_obj.posts.all()
        data['type'] = 'friends'
        data['items'] = PostSerializer(posts, many=True).data
        return Response(data=data)
'''

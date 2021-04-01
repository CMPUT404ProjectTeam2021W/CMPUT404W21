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
        data = PostSerializer(posts, many=True, context={'request' : request}).data
        return Response(data=data)

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
        followers = author_obj.followers.all()
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
        if author_obj.followers.filter(id=foreign_author_id).exists():
            data['detail'] = 'true'
        else:
            data['detail'] = 'false'
        return Response(data=data)

    def delete(self, request, author_id, foreign_author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        if author_obj.followers.filter(id=foreign_author_id).exists():
            author_obj.followers.remove(Author.objects.get(id=foreign_author_id))
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class FriendsList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        followers = author_obj.followers.all()
        following = author_obj.following.all()
        friends = [i for i in followers if i in following]
        data = dict()
        data['type'] = 'friends'
        data['items'] = AuthorSerializer(friends, many=True).data
        return Response(data=data)

class LikedList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        data = dict()
        posts = author_obj.posts.all()
        data['type'] = 'friends'
        data['items'] = PostSerializer(posts, many=True).data
        return Response(data=data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import get_object_or_404
from ..models import *
from ..serializers import *
from django.db.models import CharField, Value

class AuthorList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        authors = Author.objects.all()
        data = AuthorSerializer(authors, many=True).data
        return Response(data)

class PostList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        posts = Post.objects.all()
        data = PostSerializer(posts, many=True, context={'request' : request}).data
        return Response(data=data)

class AuthorDetails(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    def get(self, request, author_id):
        author_obj = get_object_or_404(Author, id=author_id)
        data = AuthorSerializer(author_obj).data
        return Response(data=data)
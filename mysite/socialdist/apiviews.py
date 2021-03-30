from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

class AuthorList(APIView):
    def get(self, request):
        authors = Author.objects.all()
        data = AuthorSerializer(authors, many=True).data
        return Response(data)

class PostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        data = PostSerializer(posts, many=True, context={'request' : request}).data
        return Response(data=data)


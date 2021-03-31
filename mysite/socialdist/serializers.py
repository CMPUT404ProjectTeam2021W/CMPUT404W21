from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author
        fields = ('id', 'username','github_link','friends', 'url', 'following', 'followers')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('contents', 'created_by','created_at')



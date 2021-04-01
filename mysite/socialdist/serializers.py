from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='author')
    displayName = serializers.CharField(source='username')
    github = serializers.CharField(source='github_link')
    class Meta:
        model = Author
        fields = ('type', 'id', 'url', 'displayName', 'github')

class PostSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='post')
    class Meta:
        model = Post
        fields = ('type','id','title', 'description', 'author','published', 'visibility', 'unlisted','categories')
        depth = 1

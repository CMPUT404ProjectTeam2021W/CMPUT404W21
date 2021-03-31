from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='author')
    class Meta:
        model = Author
        fields = ('type', 'id', 'url', 'username', 'github_link')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('contents', 'created_by','created_at')

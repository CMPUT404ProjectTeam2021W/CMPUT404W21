from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='author')
    displayName = serializers.CharField(source='username')
    github = serializers.CharField(source='github')
    class Meta:
        model = Author
        fields = ('type', 'id', 'url', 'displayName', 'github')

class PostSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='post')
    author = AuthorSerializer()
    
    class Meta:
        model = Post
        fields = ('type','id','title', 'description', 'author','published', 'visibility', 'unlisted','categories')

       
class AuthorDeserializer(serializers.ModelSerializer):
    username = serializers.CharField(source='displayName')

    # github = serializers.CharField(source='github')
    class Meta:
        model = Author
        fields = ('id', 'url', 'username', 'github')

class PostDeserializer(serializers.ModelSerializer):

    author = AuthorDeserializer()
    origin = serializers.ReadOnlyField(default='https://chatbyte.herokuapp.com/')
    class Meta:
        model = Post
        fields = ('id','title', 'description', 'author','published', 'visibility', 'unlisted','categories', 'origin')
 
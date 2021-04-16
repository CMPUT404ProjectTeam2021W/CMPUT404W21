from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *


class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='author')
    displayName = serializers.CharField(source='username')
    id = serializers.SerializerMethodField('replace_id_with_url')
    host = serializers.SerializerMethodField('get_host')

    def replace_id_with_url(self, obj):
        return obj.url

    def get_host(self, obj):
        return "http://hermes-cmput404.herokuapp.com/"

    class Meta:
        model = Author
        fields = ('type', 'id', 'host', 'url', 'displayName', 'github')


class PostSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='post')
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('type', 'id', 'title', 'description', 'author', 'published', 'visibility', 'unlisted', 'categories')


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
        fields = ('id', 'title', 'description', 'author', 'published', 'visibility', 'unlisted', 'categories', 'origin')


class CommentSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='comment')
    author = AuthorSerializer(read_only=True)
    contentType = serializers.ReadOnlyField(default='text/markdown')

    class Meta:
        model = Comment
        fields = ('type', 'author', 'comment', 'contentType', 'published', 'id')


class LikeSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(default='Like')
    summary = serializers.SerializerMethodField('get_summary')
    author = AuthorSerializer(read_only=True)
    object = serializers.SerializerMethodField('get_object_address')

    def get_summary(self, obj):
        return obj.author.username + " Likes your post"

    def get_object_address(self, obj):
        return "http://hermes-cmput404.herokuapp.com/author/" + str(obj.author.id) + "/posts/" + str(obj.object.id)

    class Meta:
        model = Like
        fields = ('summary', 'type', 'author', 'object')

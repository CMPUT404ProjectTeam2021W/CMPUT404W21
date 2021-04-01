from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author
        fields = ('id', 'username','github_link','friends', 'url', 'following', 'followers')
        #these dont work =(
        def restore_object(self, attrs, instance = None):
            if instance is not None:
                instance.id = attrs.get('id', instance.id)
                instance.username = attrs.get('username', instance.username)
                instance.github_link = attrs.get('github_link', instance.github_link)
                instance.url = attrs.get('url', instance.url)
                #instance.friends = attrs.get('friends', instance.friends)
                #instance.following = attrs.get('following', instance.following)
                #instance.followers = attrs.get('followers', instance.followers)
            return Author(**attrs)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('contents', 'created_by','created_at')
        #these dont work =(
    def restore_object(self, attrs, instance = None):
        if instance is not None:
            instance.contents = attrs.get('contents', instance.contents)
            instance.created_at = attrs.get('created_at', instance.created_at)
            instance.created_by = attrs.get('created_by', instance.created_by)
            return instance
        return Post(**attrs)


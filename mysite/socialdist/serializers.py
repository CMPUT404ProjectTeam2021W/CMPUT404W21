from rest_framework import serializers

from .models import *

class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'username','github_link','friends')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('contents', 'created_by','created_at')

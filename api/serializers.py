from rest_framework import serializers

from blog.models import Post
from user.models import Channel


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('name', 'description', 'post_text', 'author', 'date_created')


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ('name', 'description', 'owner')

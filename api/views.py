from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from api.permissions import BaseCustomPermission
from api.serializers import PostSerializer, ChannelSerializer
from blog.models import Post
from user.models import Channel


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [BaseCustomPermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer

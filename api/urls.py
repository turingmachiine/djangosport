from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, ChannelViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='api-post')
router.register(r'channels', ChannelViewSet, basename='api-channel')
urlpatterns = router.urls


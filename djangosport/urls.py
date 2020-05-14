"""djangosport URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAuthenticated

from blog.views import search
from news.views import RootView
from user.views import profile_view, ChannelDetailView, create

docs_schema_view = get_schema_view(
    openapi.Info(
        title='Projects API',
        default_version=f'v1',
    ), url='http://localhost:8000/docs/swagger', public=False, permission_classes=(IsAuthenticated, ),
)


urlpatterns = [
    path('', RootView.as_view(), name='root'),
    path('profile/', profile_view, name='profile'),
    path('auth/', include('user.urls')),
    path('channel/<int:pk>', ChannelDetailView.as_view(), name='channel-detail'),
    path('channel/create', create, name='channel-create'),
    path('news/', include('news.urls')),
    path('teams/', include('team.urls')),
    path('players/', include('player.urls')),
    path('posts/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('search/', search, name='search'),
    path('api/', include('api.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    docs_urls = [
        path('swagger/', docs_schema_view.with_ui('swagger'), name='schema-swagger-ui'),

    ]
    urlpatterns += [path('docs/', include(docs_urls))]

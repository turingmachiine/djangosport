from django.contrib import admin
from django.contrib.admin import ModelAdmin

from news.models import News, NewsComment

@admin.register(NewsComment)
class NewsCommentAdmin(ModelAdmin):
    list_display = ['comment_text',
                    'author',
                    'get_news',
                    'date_created']
    list_filter = ['author', 'news__headline']

    date_hierarchy = 'date_created'

    def get_news(self, obj):
        return obj.news.headline
    get_news.short_description = "News"
    get_news.admin_order_field = "news__name"


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ['headline',
                    'source',
                    'date_created',
                    'is_breaking']
    date_hierarchy = 'date_created'

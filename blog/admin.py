from django.contrib import admin


from django.contrib.admin import ModelAdmin, StackedInline
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.contrib.admin import ModelAdmin

from blog.models import Post, PostComment

@admin.register(PostComment)
class PostCommentAdmin(ModelAdmin):
    list_display = ['comment_text',
                    'author',
                    'get_post',
                    'date_created']
    list_filter = ['author', 'post__name']

    date_hierarchy = 'date_created'

    def get_post(self, obj):
        return obj.post.name
    get_post.short_description = "Post"
    get_post.admin_order_field = "post__name"


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ['name',
                    'description',
                    'author',
                    'date_created']
    list_filter = ['author']
    date_hierarchy = 'date_created'

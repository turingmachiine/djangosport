from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from django.contrib.auth import get_user_model

from user.models import Channel

@admin.register(get_user_model())
class UserAdmin(ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_confirmed', 'is_superuser']
    list_filter = ['is_confirmed', 'is_superuser']
    date_hierarchy = 'date_joined'

@admin.register(Channel)
class ChannelAdmin(ModelAdmin):
    list_display = ['name',
                    'owner',
                    'description',
                    'get_followers']

    list_filter = ['owner__username']
    def get_followers(self, obj):
        return len(obj.followers.all())
    get_followers.short_description = "Followers number"

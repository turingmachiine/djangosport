from django.contrib import admin
from django.contrib.admin import ModelAdmin

from player.models import Player, PlayerStats


@admin.register(Player)
class PlayerAdmin(ModelAdmin):
    list_display = ['get_name',
                    'get_team',
                    'nationality']
    list_filter = ['team__name', 'nationality']

    def get_name(self, obj):
        return obj.first_name + " " + obj.last_name
    get_name.short_description = "Player"

    def get_team(self, obj):
        return obj.team.name
    get_team.short_description = "Team"
    get_team.order_field = 'team__name'


@admin.register(PlayerStats)
class PlayerStatsAdmin(ModelAdmin):
    list_display = ['get_player',
                    'season',
                    'games',
                    'goals',
                    'assists',
                    'avr_score']

    list_filter = ['player__last_name']
    def get_player(self, obj):
        return obj.player.first_name + " " + obj.player.last_name
    get_player.short_description = "Player"
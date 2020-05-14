from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from team.models import Team, TeamStats, Standings


@admin.register(Team)
class TeamAdmin(ModelAdmin):
    list_display = ['name',
                    'birth_year',
                    'owner']


@admin.register(TeamStats)
class TeamStatsAdmin(ModelAdmin):
    list_display = ['get_team',
                    'year',
                    'place',
                    'wins',
                    'draws',
                    'loses',
                    'points',
                    'goals',
                    'opp_goals']

    def get_team(self, obj):
        return obj.team.name
    get_team.short_description = "Team"

    list_filter = ['team__name', 'year']


@admin.register(Standings)
class StandingsAdmin(ModelAdmin):
    list_display = ['get_team',
                    'wins',
                    'draws',
                    'loses',
                    'points',
                    'goals',
                    'opp_goals']

    def get_team(self, obj):
        return obj.team.name
    get_team.short_description = "Team"

    list_filter = ['team__name']


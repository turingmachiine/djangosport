from django.shortcuts import render
from django.views.generic import ListView, DetailView

from team.models import Team, TeamStats, Standings


class TeamListView(ListView):
    model = Team


class TeamDetailView(DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_stats'] = TeamStats.objects.filter(team=super().get_object())
        context['standings'] = Standings.objects.all().order_by('-points')
        return context

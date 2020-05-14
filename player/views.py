from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from player.models import Player, PlayerStats


class PlayerListView(ListView):
    model = Player

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET.__contains__('team_id'):
            team_id = self.request.GET.__getitem__('team_id')
            queryset = queryset.filter(team_id=team_id)
        return queryset


class PlayerDetailView(DetailView):
    model = Player

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player_stats'] = PlayerStats.objects.filter(player=super().get_object())
        return context

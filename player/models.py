from django.db import models

from team.models import Team


class Player(models.Model):

    class Position(models.TextChoices):
        PL = "PLAYER"
        GK = "GOALKEEPER"
        RB = "RIGHT BACK"
        CB = "CENTRAL BACK"
        LB = "LEFT BACK"
        DM = "DEFENSIVE MIDFIELDER"
        CMF = "CENTRAL MIDFIELDER"
        LMF = "LEFT MIDFIELDER"
        RMF = "RIGHT MIDFIELDER"
        AMF = "ATTACKING MIDFIELDER"
        ST = "STRIKER"
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=255,
                                choices=Position.choices, default=Position.PL)
    nationality = models.CharField(max_length=255)
    birth_date = models.DateTimeField()
    birth_city = models.CharField(max_length=255)


class PlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    season = models.CharField(max_length=255)
    games = models.IntegerField()
    goals = models.IntegerField()
    assists = models.IntegerField()
    avr_score = models.FloatField()

    class Meta:
        verbose_name = "Player stats"
        verbose_name_plural = "Player stats"

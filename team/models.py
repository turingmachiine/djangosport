import uuid

from django.db import models


def extract_file_extension(filename):
    return filename.split('.')[1]


def upload_img_file(instance, filename: str) -> str:
    team_id = getattr(instance, 'id', None)

    new_filename = '.'.join((str(uuid.uuid4()), extract_file_extension(filename)))
    return f'teams/{team_id}/{new_filename}'


class Team(models.Model):
    name = models.CharField(max_length=255)
    birth_year = models.IntegerField()
    logo = models.ImageField(upload_to=upload_img_file)
    titles_number = models.IntegerField()
    owner = models.CharField(max_length=255)
    history = models.TextField()


class TeamStats(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    year = models.IntegerField()
    place = models.IntegerField()
    wins = models.IntegerField()
    draws = models.IntegerField()
    loses = models.IntegerField()
    points = models.IntegerField()
    goals = models.IntegerField()
    opp_goals = models.IntegerField()

    class Meta:
        verbose_name = "Team stats"
        verbose_name_plural = "Team stats"


class Standings(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    wins = models.IntegerField()
    draws = models.IntegerField()
    loses = models.IntegerField()
    points = models.IntegerField()
    goals = models.IntegerField()
    opp_goals = models.IntegerField()

    class Meta:
        verbose_name = "Standings"
        verbose_name_plural = "Standings"

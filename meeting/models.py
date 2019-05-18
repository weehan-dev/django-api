from django.db import models
from user.models import Profile

class Team(models.Model):
    CHOOSING = (
        ("two-people", "2명"),
        ("three-people", "3명")
    )
    team_longitude = Profile.longitude
    team_latitude = Profile.latitude
    team_type = models.CharField("team type", choices=CHOOSING, max_length=1)
# Create your models here

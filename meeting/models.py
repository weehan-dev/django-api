from django.db import models

class Team(models.Model):
    CHOOSING = (
        (2, "2명"),
        (3, "3명")
    )


    team_latitude = models.DecimalField(decimal_places=7, max_digits=9)
    team_longitude = models.DecimalField(decimal_places=7, max_digits=10)
    team_type = models.PositiveSmallIntegerField("team type", choices=CHOOSING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

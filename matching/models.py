from django.db import models

# Create your models here.


class Team(models.Model):

    versus = models.IntegerField()

    avg_age = models.IntegerField(null=False)
    location = models.CharField(max_length=10)
    hope_age = models.IntegerField(default=None, null=True)

    is_matched = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

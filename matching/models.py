from django.db import models

# Create your models here.


DAY = (
    ('월요일', 'mon'),
    ('화요일', 'tue'),
    ('수요일', 'wed'),
    ('목요일', 'thur'),
    ('금요일', 'fri'),
    ('토요일', 'sat'),
    ('일요일', 'sun')
)


class Team(models.Model):

    versus = models.IntegerField()

    leader = models.PositiveIntegerField(null=False)

    day = models.CharField(max_length=5, choices=DAY)
    avg_age = models.IntegerField(null=False)
    location = models.CharField(max_length=10)
    hope_age = models.IntegerField(default=None, null=True)

    is_matched = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

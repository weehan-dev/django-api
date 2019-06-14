from django.db import models
from user.models import Profile
# Create your models here.


class Notification(models.Model):

    TYPE = (
        ('msg', 'Message'),
        ('follow', 'Follow'),
        ('team', 'Team'),
        ('match', 'Match')
    )

    creator = models.ForeignKey(Profile)
    notification_type = models.CharField(max_length=10, choices=TYPE)
    comment = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

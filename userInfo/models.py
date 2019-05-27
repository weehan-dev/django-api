from django.db import models

# Create your models here.


class Token(models.Model):

    token = models.CharField(max_length=10, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(unique=True, max_length=30, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

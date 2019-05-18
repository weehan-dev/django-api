from rest_framework import serializers
from user.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        Model = Profile
        field = {"name", "avatar", "user"}
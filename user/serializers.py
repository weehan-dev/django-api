from rest_framework import serializers
from user.models import GENDER, UNIV_LIST, User


class UserProfileSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = '__all__'

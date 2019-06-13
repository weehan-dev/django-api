from rest_framework import serializers
from matching.models import Team
from user.models import Profile
from user.serializers import UserSerializer as user_UserSerializer


class NestedMembersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['name', 'gender', 'univ', 'avatar', 'age']


class TeamMembersSerializer(serializers.ModelSerializer):

    members = NestedMembersSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"


class UserAndProfileSerializer(serializers.ModelSerializer):
    user = user_UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"

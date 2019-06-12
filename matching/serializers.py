from rest_framework import serializers
from matching.models import Team
from user.models import Profile


class NestedMembersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['name', 'gender', 'univ', 'avatar', 'age']


class TeamMembersSerializer(serializers.ModelSerializer):

    members = NestedMembersSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


from rest_framework import serializers
from matching.models import Team


class CreateTeamSerializer(serializers.ModelSerializer):

    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


from rest_framework import serializers

from user.models import Profile, User
from user.serializers import UserSerializer



class NestedOnlyUsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class LittleProfileInfoSerializer(serializers.ModelSerializer):

    user = NestedOnlyUsernameSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'name', 'age', 'avatar', 'gender', 'id']




class FollowerSerializer(serializers.ModelSerializer):

    follower = LittleProfileInfoSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ['follower']


class FollowingSerializer(serializers.ModelSerializer):

    following = LittleProfileInfoSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ('following', )


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    avatar = serializers.ImageField(allow_null=True, default=None)
    follower = LittleProfileInfoSerializer(read_only=True, many=True)
    following = LittleProfileInfoSerializer(read_only=True, many=True)

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    class Meta:
        model = Profile
        fields = "__all__"


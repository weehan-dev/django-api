from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from user.models import User, Profile


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=7, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class ProfileSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        profile = Profile.objects.create(**validated_data)
        return profile

    class Meta:
        model = Profile,
        fields = '__all__'


class NestedProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class NestedUserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class LoginSerializer(TokenObtainPairSerializer):
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        #data['user'] = NestedUserInfoSerializer(self.user)
        #data['profile'] = NestedProfileSerializer(read_only=True)

        return data

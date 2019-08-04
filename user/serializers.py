from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from user.models import User, Profile

class ChangeUserInfoSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, min_length=7, write_only=True)

    def validate(self, attrs):
            raise serializers.ValidationError('이전 패스워드가 맞지 않습니다.')

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'email']


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=7, write_only=True)

    has_team = serializers.BooleanField(read_only=True)
    has_profile = serializers.BooleanField(read_only=True)
    is_certificated =serializers.BooleanField(read_only=True)
    is_suspended =serializers.BooleanField(read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'has_team', 'has_profile', 'is_certificated', 'is_suspended']


class NestedProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['account'] = UserSerializer(self.user).data
        try:
            profile = Profile.objects.get(user=self.user)
            data['profile'] = NestedProfileSerializer(profile).data
            return data
        except Profile.DoesNotExist:
            return data

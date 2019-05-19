from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer, LoginSerializer, ProfileSerializer

# Create your views here.

User = get_user_model()


class Signup(APIView):
    permission_classes = [AllowAny]
    """
    create User
    """
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)


class YHDTokenObtainPairView(TokenObtainPairView):
    serializer_class = LoginSerializer


class Profile(APIView):

    def post(self, request, format=None):
        """
        :body: user, name, gender, univ, latitude, longitude, avatar, height, weight, religion, is_smoker:
        :return: json(success, message, data):
        """

        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            profile = serializer.save()
            if profile:
                Response(status=status.HTTP_201_CREATED, data=profile)
            Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        Response(status=status.HTTP_406_NOT_ACCEPTABLE)

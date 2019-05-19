from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer, LoginSerializer

# Create your views here.

User = get_user_model()


class Signup(APIView):
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

from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth import get_user_model

from user.serializers import UserSerializer, LoginSerializer

# Create your views here.

User = get_user_model()


class ChangeAccountInformation(APIView):
    """
    로그인 이후 계정정보 변경할 때
    """
    def put(self, request, format=None):
        old_password = request['PUT']['old_password']
        if not request.user.check_password(old_password):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='이전 비밀번호가 맞지 않습니다.')

        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            account = serializer.save()
            if account:
                return Response(status=status.HTTP_202_ACCEPTED, data=serializer.data)
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)



class Signup(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        create User
        """
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



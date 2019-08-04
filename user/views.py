from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from user.serializers import UserSerializer, LoginSerializer
from django.shortcuts import get_object_or_404


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


"""
유진 / 회원 정보 수정 할거임
"""
class DeleteUser(APIView):
    """
    회원 탈퇴
    """
    def delete(self, request, id, format=None):
        user = get_object_or_404(User, id=id)
        # 비밀번호 요구
        password = request.data['password']
        if not request.user.check_password(password):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='비밀번호가 맞지 않습니다.')
        else:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={"username" : user.username, "password" : user.password, "success": True})

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserProfileSerializer
# Create your views here.


@api_view(['GET', 'POST'])
def user_info(request):
    pass


class ManageUser (APIView):

    '''
    User만들기, 유저 정보 보기, 유저 정보 수정, 유저 정보 삭제 클래스,
    GET, POST, UPDATE, DELETE
    '''

    @staticmethod
    def get_user(username, email):
        try:
            if email:
                found_user = User.objects.get(username=username, email=email)
            else:
                found_user = User.objects.get(username=username)
            return found_user

        except User.DoesNotExist:
            return None

    def get(self, request, format=None):

        username = request.query_params.get('username')
        email = request.query_params.get('email')
        user = self.get_user(username=username, email=email)

        if user:
            serializer = UserProfileSerializer(user)
            return Response(data=serializer.data)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

# Create your views here.
from django.db import models
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User, Profile
from userInfo.serializers import ProfileSerializer


class HandleProfile(APIView):
    def get(self, request, id, format=None):
        user = get_object_or_404(User, id=id)
        profile = get_object_or_404(Profile, user=user)

        serializer = ProfileSerializer(profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        user = get_object_or_404(User, id=id)
        if user != request.user:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="타인의 프로필을 수정할 수 없습니다.")

        profile = get_object_or_404(Profile, user=user)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)

    def post(self, request, id, format=None):
        """
        :body: name, gender, univ, latitude, longitude, avatar, height, weight, religion, is_smoker:
        :return: json(success, message, data):
        """
        user = get_object_or_404(User, id=id)
        if user != request.user:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="타인의 프로필을 생성할 수 없습니다.")

        try:
            Profile.objects.get(user=user)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="이미 프로필이 존재합니다.")
        except Profile.DoesNotExist:
            serializer = ProfileSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                profile = serializer.save()
                if profile:
                    profile.user = request.user
                    profile.save()
                    print(request.user.profile)

                    data = ProfileSerializer(profile)
                    return Response(status=status.HTTP_201_CREATED, data=data.data)
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED, data=serializer.errors)

            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data=serializer.errors)

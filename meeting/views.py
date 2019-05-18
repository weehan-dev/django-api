from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from meeting.serializers import ProfileSerializer
class implement():

class teammaking():
    def post(self, request, format=None):
        serializer = ProfileSerializer.objects.get(data=request.data)
        if serializer.is_matched():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

class complete():

# Create your views here.

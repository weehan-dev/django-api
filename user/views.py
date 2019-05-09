from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . models import User

# Create your views here.


@api_view(['GET', 'POST'])
def user_info(request):
    pass



class Username(APIView):

    def get(self, request, format=None):
        id = request.m
        User.objects.get()

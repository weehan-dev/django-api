from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from meeting.serializers import ProfileSerializer
from user.models import User
from meeting.models import Team
from meeting.form import TeamForm
class ShowSearchingProfile():
    def post(self, request, format=None):
        term = 1 # 리퀘스트에서 검색 용어 찾아야 함
        user = User.objects.get(username=term)
        if user:
            if not user.is_matched:
                serializer = ProfileSerializer(user.profile)
                return Response(status=status.HTTP_200_OK, data=serializer.data)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)# 유저가 이미 매칭 중이라는 것을 알려줄 리턴
        return Response(status=status.HTTP_404_NOT_FOUND)# 유저가 없을 때 리턴
class TeamMaking():
    def team_update(request):
        team = request.team
        if not team.is_owner_or_manager(request.user):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        if request.method == "POST":
            form = TeamForm(request.POST, instance=team)
            if form.is_valid():
                form.save()
                return Response(team.get_absolute_url())
        else:
            form = TeamForm(instance=team)
        return Response(request)
#   Create your views here.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from matching.models import Team
from user.models import Profile, User
# Create your views here.


class InviteTeam(APIView):

    @staticmethod
    def make_user_object(id):
        id *= 1
        return User.objects.get(id=id)

    @staticmethod
    def is_friend(user, target):
        try:
            user.profile.following.get(target)

    def post(self, request, format=None):
        if request.user.has_team:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'message': '이미 팀에 속해있습니다..'})
        else:
            members_id = request.POST['members']
            try:
                members = map(lambda id: self.make_user_object(id), members_id.strip('[]').split(', '))


            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': '존재하지 않는 유저입니다.'})

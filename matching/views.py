from functools import reduce

from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from matching.models import Team
from user.models import User, Profile
from matching.serializers import TeamMembersSerializer, UserAndProfileSerializer
# Create your views here.


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def reset_team(request):
    user = request.user.profile
    user.team = None
    user.save()
    serializer = UserAndProfileSerializer(user)
    return Response(status=status.HTTP_200_OK, data=serializer.data)



class InviteTeam(APIView):

    @staticmethod
    def make_user_object(id):
        id *= 1
        return User.objects.get(id=id)

    @staticmethod
    def is_friend(user, target):
        try:
            if len(user.profile.following.filter(id=target.profile.id)):
                return True
            return False
        except:
            return False

    def post(self, request, format=None):
        if request.user.has_team:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'message': '이미 팀에 속해있습니다.'})
        if not request.user.has_profile:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'message': '프로필을 먼저 설정해주세요.'})

        members_id = request.POST['members']
        try:
            members = list(map(lambda id: self.make_user_object(id), members_id.strip('[]').split(', ')))

            for target in members:
                if target == request.user:
                    raise Exception('본인을 추가할 수 없습니다.')
                if not target.has_profile:
                    raise Exception('미팅 팀 모두 프로필을 설정해야 합니다.')
                if target.has_team:
                    raise Exception('이미 팀에 속한 유저가 있습니다.')

                if not self.is_friend(request.user, target):
                    raise Exception('친구 목록에 없는 유저입니다.')
                if not self.is_friend(target, request.user):
                    raise Exception('상대방의 친구 목록에 유저가 없습니다.')

            age_sum = 0
            team = Team.objects.create(location=request.user.profile.state, hope_age=request.POST['hopeAge'], versus=0, avg_age=0)
            members.append(request.user)
            for user in members:
                age_sum += user.profile.age
                team.versus += 1
                team.members.add(user.profile)
                user.has_team = True
                user.save()

            team.avg_age = round(age_sum / len(members))
            team.save()
            serializer = TeamMembersSerializer(team)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': '존재하지 않는 유저입니다.'})

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': str(e)})


class LeaveTeam(APIView):
    def delete(self, request):
        try:
            user = request.user
            if not user.has_team:
                raise Exception('팀이 존재하지 않습니다.')
            team = user.profile.team
            team.members.remove(user.profile)
            team.versus -= 1
            team.avg_age = round(reduce(lambda x, y: x + y, team.members.all(), 0) / team.versus)
            team.save()

            user.has_team = False
            user.save()

            if not team.members.all():
                team.delete()

            serializer = TeamMembersSerializer(team)
            return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.data)

        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': '해당 팀이 존재하지 않습니다.'})

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))

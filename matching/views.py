from functools import reduce

from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from matching.models import Team
from user.models import User, Profile
from matching.serializers import TeamMembersSerializer, UserAndProfileSerializer
# Create your views here.


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def reset_team(request):

    user = request.user

    user.profile.team = None
    user.has_team = False

    user.save()
    serializer = UserAndProfileSerializer(user.profile)
    return Response(status=status.HTTP_200_OK, data=serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def view_team(request, team_id):

    try:
        team = Team.objects.get(id=team_id)
        serializer = TeamMembersSerializer(team)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'message': '해당 팀이 없습니다.'})


class TeamMemberHandler(APIView):
    @staticmethod
    def is_friend(user, target):
        try:
            if len(user.profile.following.filter(id=target.profile.id)):
                return True
            return False
        except:
            return False

    def put(self, request, id):
        """
        팀원 추가
        :param id: 유저 아이디
        :return:
        """
        try:
            if not request.user.has_team:
                raise Exception('팀이 없습니다.')
            team = request.user.profile.team
            if request.user.profile.id != team.leader:
                raise Exception('팀 리더만 팀 맴버를 추가할 수 있습니다.')
            if team.versus >= 4:
                raise Exception('최대 4명까지 가능합니다.')
            target_user = User.objects.get(id=id)
            if target_user.has_team:
                raise Exception('이미 팀이 존재하는 유저입니다.')
            if not target_user.has_profile:
                raise Exception('상대방의 프로필이 없습니다.')
            if not self.is_friend(request.user, target_user):
                raise Exception('상대방이 유저의 친구가 아닙니다.')
            if not self.is_friend(target_user, request.user):
                raise Exception('상대방의 친구 목록에 유저가 없습니다.')

            team.members.add(target_user.profile)
            temp = team.avg_age * team.versus
            team.versus += 1
            temp += target_user.profile.age
            team.avg_age = temp / team.versus

            team.save()

            target_user.has_team = True
            target_user.save()

            serializer = TeamMembersSerializer(team)

            return Response(status=status.HTTP_202_ACCEPTED, data=serializer.data)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': '해당 유저가 없습니다.'})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))

    def delete(self, request, id):
        """
        팀원 삭제
        :param id: 유저 아이디
        :return:
        """

        try:
            if request.user.id == id:
                raise Exception('자신을 강퇴할 수 없습니다.')
            if not request.user.has_team:
                raise Exception('팀이 없습니다.')
            team = request.user.profile.team
            target_user = User.objects.get(id=id)
            if not target_user.has_team:
                raise Exception('상대방 팀이 없습니다.')
            if target_user.profile.team_id != team.id:
                raise Exception('같은 팀에 없는 유저입니다.')
            if team.leader != request.user.profile.id:
                raise Exception('팀장만이 강퇴할 수 있습니다.')

            team.members.remove(target_user)
            target_user.has_team = False
            target_user.save()

            temp = team.avg_age * team.versus
            temp -= target_user.profile.age
            team.versus -= 1
            team.avg_age = temp / team.versus
            team.save()

            serializer = TeamMembersSerializer(team)

            return Response(status=status.HTTP_202_ACCEPTED, data=serializer.data)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': '없는 유저입니다.'})

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))


class TeamHandler(APIView):

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

    def put(self, request, format=None):
        """
        팀 location, hope_age 수정하는 함수
        :return:
        """

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
            team = Team.objects.create(location=request.user.profile.state, hope_age=request.POST['hopeAge'], versus=0, avg_age=0, leader=request.user.profile.id)
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

    def delete(self, request, format=None):
        try:
            user = request.user
            if not user.has_team:
                raise Exception('팀이 존재하지 않습니다.')
            team = user.profile.team
            team.members.remove(user.profile)
            team.versus -= 1

            if not team.versus:
                team.delete()
                user.has_team = False
                user.save()
                return Response(status=status.HTTP_204_NO_CONTENT, data={'message': '팀이 삭제되었습니다.'})
            else:
                team.avg_age = round(reduce(lambda x, y: x + y, [i for i in map(lambda profile: profile.age, team.members.all())], 0) / team.versus)
                team.save()

                user.has_team = False
                user.save()

                serializer = TeamMembersSerializer(team)
                return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.data)

        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': '해당 팀이 존재하지 않습니다.'})

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(e))

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from matching.models import Team
from user.models import User
from matching.serializers import TeamMembersSerializer
# Create your views here.


class InviteTeam(APIView):

    @staticmethod
    def make_user_object(id):
        id *= 1
        return User.objects.get(id=id)

    @staticmethod
    def is_friend(user, target):
        try:
            friend = user.profile.following.get(target)
            if friend:
                return True
            return False
        except:
            return False

    def post(self, request, format=None):
        if request.user.has_team:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={'message': '이미 팀에 속해있습니다.'})
        else:
            members_id = request.POST['members']
            try:
                print(members_id)
                members = list(map(lambda id: self.make_user_object(id), members_id.strip('[]').split(', ')))

                for target in members:
                    if not self.is_friend(request.user, target):
                        raise Exception('친구 목록에 없는 유저입니다.')
                    if not self.is_friend(target, request.user):
                        raise Exception('상대방의 친구 목록에 유저가 없습니다.')

                age_sum = 0
                team = Team(location=request.user.profile.state, hope_age=request.POST['hopeAge'])
                members.append(request.user)
                for user in members:
                    age_sum += user.profile.age
                    user.profile.team = team
                    user.has_team = True
                    user.save()
                    user.profile.save()

                team.avg_age = round(age_sum / len(members))
                team.versus = len(members)
                serializer = TeamMembersSerializer(team)

                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED, data=serializer.data)
                else:
                    raise Exception('유효하지 않은 요청입니다.')

            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': '존재하지 않는 유저입니다.'})

            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': e})


class LeaveTeam(APIView):
    def delete(self, request):
        try:
            user = request.user
            if not user.has_team:
                raise Exception('팀이 존재하지 않습니다.')
            team = user.profile.team
            team.members.remove(user)

            serializer = TeamMembersSerializer(team)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT, data=serializer.data)

        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': '해당 팀이 존재하지 않습니다.'})

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e)

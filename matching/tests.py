from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase
from matching import views as matching_views
from django.urls

# Create your tests here.
from user.models import User

class TeamTest(APITestCase):
    def test_invite_team(self):
        pass


factory = APIRequestFactory()

"""
InviteTeamTest
"""

user = User.objects.get(id=1)
view = matching_views.InviteTeam.as_view()

InviteTeamRequest = factory.post('/team/', {
    'members': '[1, 2, 3, 4]'
}, format='json')
force_authenticate(InviteTeamRequest, user=user, token=user.auth_token)
response = view(InviteTeamRequest)

"""
LeaveTeamTest
"""

LeaveTeamRequest = factory.delete('/team/leave/', format='json')

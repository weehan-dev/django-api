from django.urls import path
from matching import views

urlpatterns = [
    path('team/', views.InviteTeam.as_view(), name="make_team"),
    path('team/leave/', views.LeaveTeam.as_view(), name='leave_team'),
    path('reset/', views.reset_team, name='dev_reset'),
    path('<team_id>/', views.view_team, name='dev_view_team')
]
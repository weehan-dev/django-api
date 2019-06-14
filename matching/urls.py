from django.urls import path
from matching import views

urlpatterns = [
    path('team/', views.TeamHandler.as_view(), name="team_handler"),
    path('team/<team_id>/', views.view_team, name='dev_view_team'),
    path('team/member/<int:id>/', views.TeamMemberHandler.as_view(), name='team_member_handler'),
    path('reset/', views.reset_team, name='dev_reset'),
]

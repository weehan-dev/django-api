from django.urls import path
from matching import views

urlpatterns = [
    path('team/', views.InviteTeam.as_view(), name="make_team"),
    path('team/leave/', views.LeaveTeam.as_view(), name='leave_team'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('team/', views.teammaking.as_view(), name='team_making'),
    path('invite/', views.inviting.as_view(), name="inviting"),
    path('complete/', views.complete.as_view(), name="complete")
]
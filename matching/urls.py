from django.urls import path
from matching.views import MakeTeam

urlpatterns = [
    path('try/', MakeTeam.as_view(), name="try_match"),

]
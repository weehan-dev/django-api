from django.urls import path, include
from userInfo.views import HandleProfile

urlpatterns = [
    path('<int:id>/', HandleProfile.as_view(), name="profile")
]

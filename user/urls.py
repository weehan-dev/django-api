from django.urls import path
from . import views

urlpatterns = [
    path('', views.ManageUser, name="auth")
]
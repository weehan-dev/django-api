from django.urls import path, include
from userInfo import views as users_views
from user import views as account_views
urlpatterns = [
    path('<int:id>/', users_views.HandleProfile.as_view(), name="profile"),
    path('reset/', account_views.ChangeAccountInformation.as_view(), name="account_modify")
]

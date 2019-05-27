from django.urls import path, include
from userInfo import views as users_views
from user import views as account_views

urlpatterns = [
    path('<int:id>/', users_views.HandleProfile.as_view(), name="profile"),
    path('reset/', account_views.ChangeAccountInformation.as_view(), name="account_modify"),
    path('<int:id>/token/', users_views.SendMailToken.as_view(), name='send_email'),
    path('<int:id>/verification/', users_views.VerifyMailToken.as_view(), name='verify_email')
]

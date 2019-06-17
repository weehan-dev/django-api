from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from userInfo import views as users_views
from notification import views as notification_views
from user import views as account_views

urlpatterns = [
    path('<int:id>/api/validate-token/', users_views.validate_token, name="token_check"),
    path('<int:id>/', users_views.HandleProfile.as_view(), name="profile"),
    path('reset/', account_views.ChangeAccountInformation.as_view(), name="account_modify"),
    path('<int:id>/token/', users_views.SendMailToken.as_view(), name='send_email'),
    path('<int:id>/verification/', users_views.VerifyMailToken.as_view(), name='verify_email'),
    path('<int:id>/notification/', notification_views.set_notification_token, name='set_notification_token'),
    #path('profile/map/', users_views.map_view, name="map_view"),
    path('follow/<int:target_id>/', users_views.FollowUser.as_view(), name="following_user"),
    path('follower/list/', users_views.FollwerList.as_view(), name='follower_list'),
    path('following/list/', users_views.FollowingList.as_view(), name='following_list')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
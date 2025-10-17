from django.urls import  path
from .views import *
from ..posts.views import FollowUserView, UnfollowUserView

urlpatterns = [
    path("login/", LoginView.as_view(), name='login-view'),
    path("register/", RegistrationView.as_view(), name='register'),
    path("profile/", UserProfileView.as_view(), name='Profile'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
]
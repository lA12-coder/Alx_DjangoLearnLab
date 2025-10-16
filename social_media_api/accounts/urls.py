from django.urls import  path
from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name='login-view'),
    path("register/", RegistrationView.as_view(), name='register'),
    path("profile/", UserProfileView.as_view(), name='Profile')
]
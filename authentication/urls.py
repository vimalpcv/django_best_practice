from django.urls import path, include
from authentication.views import *
from dj_rest_auth.registration.views import SocialAccountListView, SocialAccountDisconnectView

urlpatterns = [
    path("register/", CustomRegisterView.as_view(), name="account_signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("refresh/", RefreshTokenView.as_view(), name="refresh"),

    # social login connect
    path("connect/google/", GoogleConnect.as_view(), name="google_connect"),
    path("social-accounts/", SocialAccountListView.as_view(), name="socialaccount_connections",),
    path('social-accounts/<int:pk>/disconnect/', SocialAccountDisconnectView.as_view(), name='social_account_disconnect'),

    # social login
    path("login/google/", GoogleLogin.as_view(), name="google_login"),







]

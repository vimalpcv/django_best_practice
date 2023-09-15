from django.urls import path
from .views import *

urlpatterns = [
    path("", UserView.as_view(), name='user'),
    path("login/", LoginView.as_view(), name="login"),
]
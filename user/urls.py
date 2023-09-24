from django.urls import path
from user.views import *

urlpatterns = [
    path("detail/", UserDetailView.as_view(), name='user'),
]

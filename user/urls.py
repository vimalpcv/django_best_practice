from django.urls import path
from .views import *

urlpatterns = [
    path("detail/", UserDetailView.as_view(), name='user'),
]

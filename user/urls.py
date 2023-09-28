from django.urls import path
from user.views import *


urlpatterns = [
   path("details/", UserDetailView.as_view(), name='user_detail'),

]

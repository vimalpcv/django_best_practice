"""
URL configuration for common project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import *
from user import urls as user_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    # Health Check
    path('', HealthCheck.as_view(), name='health'),

    # Authentication
    path("api/register/", CustomRegisterView.as_view(), name="account_signup"),
    path("api/login/", CustomLoginView.as_view(), name="login"),
    path("api/logout/", CustomLogoutView.as_view(), name="logout"),
    path("api/refresh/", RefreshTokenView.as_view(), name="refresh"),

    path('user/', include(user_urls)),

    # API Documentation
    path('api/docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.SOCIAL_LOGIN_ENABLED:
    urlpatterns += [
        # Authentication - social login connect
        path("api/connect/google/", GoogleConnect.as_view(), name="google_connect"),
        path("api/social-accounts/", CustomSocialAccountListView.as_view(), name="socialaccount_connections", ),
        path('api/social-accounts/<int:pk>/disconnect/', CustomSocialAccountDisconnectView.as_view(),
             name='socialaccount_disconnect'),

        # Authentication - social login
        path("api/login/google/", GoogleLogin.as_view(), name="google_login"),
]

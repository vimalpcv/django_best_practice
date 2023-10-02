from rest_framework.permissions import AllowAny, IsAuthenticated as _IsAuthenticated
from django.conf import settings
from rest_framework.authtoken.models import Token
from datetime import timedelta
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed




def method_permission_classes(permission_classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = permission_classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator


class IsAuthenticated(_IsAuthenticated):
    def has_permission(self, request, view) -> bool:
        user = request.user
        permission = False
        if super().has_permission(request, view) and user.is_active and user.organization.is_active:
            permission = True

        if not settings.JWT_AUTHENTICATION_ENABLED:
            token = Token.objects.filter(user=user).first()
            if not token:
                permission = False
            else:
                if token.created + settings.TOKEN_LIFETIME < timezone.now():
                    token.delete()
                    raise AuthenticationFailed("Token expired")

        return permission


class IsAllowedUser(IsAuthenticated):
    def __init__(self, *roles):
        self.roles = roles

    def has_permission(self, request, view) -> bool:
        user = request.user
        permission = False
        if super().has_permission(request, view):
            if self.roles:
                if user.role in self.roles:
                    permission = True
            else:
                permission = True

        return permission



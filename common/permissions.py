from rest_framework.permissions import IsAuthenticated


def method_permission_classes(permission_classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = permission_classes
            # this call is needed for request permissions
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator


class IsAllowedUser(IsAuthenticated):
    def __init__(self, *roles):
        self.roles = roles

    def has_permission(self, request, view) -> bool:
        user = request.user
        permission = False
        if super().has_permission(request, view) and user.is_active and user.organization.is_active:
            if self.roles:
                if user.role in self.roles:
                    permission = True
            else:
                permission = True

        return permission



from rest_framework.permissions import IsAuthenticated


class IsAllowedUser(IsAuthenticated):
    def __init__(self, *roles):
        self.roles = roles

    def has_permission(self, request, view):
        user = request.user
        permission = False
        if super().has_permission(request, view) and user.is_active and user.organization.is_active:
            if self.roles:
                if user.role in self.roles:
                    permission = True
            else:
                permission = True

        return permission



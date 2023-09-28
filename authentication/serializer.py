from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from common.constants import ROLES, EMPLOYEE, GENDER, MALE
from user.models import Organization
from user.serializer import UserDetailSerializer


class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom serializer for the registration endpoint.
    """
    organization = serializers.IntegerField(required=True)
    role = serializers.ChoiceField(choices=ROLES, default=EMPLOYEE)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.ChoiceField(choices=GENDER, default=MALE)

    def validate_organization(self, organization):
        """
        Check that the organization exists.
        """
        try:
            Organization.objects.get(id=organization)
        except Organization.DoesNotExist:
            raise serializers.ValidationError("The specified organization does not exist.")
        return organization

    def save(self, request):
        """
        Alter the save method to add the organization to the user.
        """
        user = super().save(request)
        user.organization = Organization.objects.get(id=self.data.get('organization'))
        user.save()
        return user


class LogoutViewSerializer(serializers.Serializer):
    """
    Serializer for the logout endpoint.
    """
    refresh = serializers.CharField()


class RefreshViewSerializer(serializers.Serializer):
    """
    Serializer for the refresh token endpoint.
    """
    refresh = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer for the login response.
    """
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserDetailSerializer()


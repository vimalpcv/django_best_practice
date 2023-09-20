from rest_framework import serializers
from user.models import User


class LoginViewSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LogoutViewSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class RefreshViewSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'first_name', 'last_name', 'email', 'username', 'is_active', 'organization'
        help_text = "Custom help text for this serializer."

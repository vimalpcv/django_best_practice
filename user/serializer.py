from rest_framework import serializers
from user.models import User, Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'description')


class UserDetailSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'organization')

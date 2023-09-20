from rest_framework import serializers


class TemplateViewSerializer(serializers.Serializer):
    field1 = serializers.CharField()
    field2 = serializers.IntegerField()
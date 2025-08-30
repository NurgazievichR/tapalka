from rest_framework import serializers

class AuthInitDataSerializer(serializers.Serializer):
    init_data = serializers.CharField()
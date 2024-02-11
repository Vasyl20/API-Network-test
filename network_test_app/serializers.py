from rest_framework import serializers
from .models import NetworkTestResult

class NetworkTestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkTestResult
        fields = '__all__'
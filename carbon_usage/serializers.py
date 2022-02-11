from rest_framework import serializers

from carbon_usage.models import Usage, UsageTypes


class UsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usage
        fields = ['user', 'usage_type', 'usage_at', 'amount']


class UsageTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageTypes
        fields = ['name', 'unit', 'factor']

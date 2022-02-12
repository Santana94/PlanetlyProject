from django_filters import rest_framework as filters

from carbon_usage.models import Usage, UsageTypes


class UsageFilter(filters.FilterSet):
    min_amount = filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = filters.NumberFilter(field_name="amount", lookup_expr='lte')
    min_usage_at = filters.DateTimeFilter(field_name="usage_at", lookup_expr='gte')
    max_usage_at = filters.DateTimeFilter(field_name="usage_at", lookup_expr='lte')

    class Meta:
        model = Usage
        fields = ('user', 'usage_type', 'min_amount', 'max_amount', 'min_usage_at', 'max_usage_at')


class UsageTypesFilter(filters.FilterSet):
    min_factor = filters.NumberFilter(field_name="factor", lookup_expr='gte')
    max_factor = filters.NumberFilter(field_name="factor", lookup_expr='lte')

    class Meta:
        model = UsageTypes
        fields = ('name', 'unit', 'min_factor', 'max_factor')

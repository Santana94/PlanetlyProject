from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from carbon_usage.filters import UsageFilter, UsageTypesFilter
from carbon_usage.models import Usage, UsageTypes
from carbon_usage.serializers import UsageSerializer, UsageTypesSerializer


class UsageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Usage instances.
    """
    serializer_class = UsageSerializer
    queryset = Usage.objects.all()
    permission_classes = (IsAuthenticated,)
    filterset_class = UsageFilter


class UsageTypesViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing UsageTypes instances.
    """
    serializer_class = UsageTypesSerializer
    queryset = UsageTypes.objects.all()
    permission_classes = (IsAuthenticated,)
    filterset_class = UsageTypesFilter

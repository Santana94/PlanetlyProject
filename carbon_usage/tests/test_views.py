import pytest
from django.urls import reverse
from rest_framework import status
from . import mommy_recipes as carbon_usage_recipes

pytestmark = pytest.mark.django_db


def test_usage_is_invalid(client):
    url = reverse('carbon-usage:usage-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_usage_is_valid(api_client):
    url = reverse('carbon-usage:usage-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


def test_usage_lists_objects(api_client):
    usages = carbon_usage_recipes.base_usage.make(_quantity=5)
    url = reverse('carbon-usage:usage-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {
            "id": usage.id,
            "user": usage.user.id,
            "usage_type": usage.usage_type.id,
            "usage_at": usage.usage_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "amount": usage.amount,
        }
        for usage in usages
    ]


def test_usage_types_is_invalid(client):
    url = reverse('carbon-usage:usage_types-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_usage_types_is_valid(api_client):
    url = reverse('carbon-usage:usage_types-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == [
        {
            "id": 100,
            "name": "electricity",
            "unit": "kwh",
            "factor": 1.5
        },
        {
            "id": 101,
            "name": "water",
            "unit": "kg",
            "factor": 26.93
        },
        {
            "id": 102,
            "name": "heating",
            "unit": "kwh",
            "factor": 3.892
        },
        {
            "id": 103,
            "name": "heating",
            "unit": "l",
            "factor": 8.57
        },
        {
            "id": 104,
            "name": "heating",
            "unit": "m3",
            "factor": 19.456
        },
    ]

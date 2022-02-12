import pytest
from django.urls import reverse
from rest_framework import status
from . import mommy_recipes as carbon_usage_recipes
from ..models import Usage

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


def test_usage_retrieve_object(api_client):
    usages = carbon_usage_recipes.base_usage.make(_quantity=5)
    usage = usages[0]
    url = reverse('carbon-usage:usage-detail', kwargs={"pk": usage.id})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "id": usage.id,
        "user": usage.user.id,
        "usage_type": usage.usage_type.id,
        "usage_at": usage.usage_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "amount": usage.amount,
    }


def test_usage_update_object_with_put(api_client, user):
    usages = carbon_usage_recipes.base_usage.make(_quantity=5)
    usage = usages[0]
    data = {
        "user": user.id,
        "usage_type": 101,
        "usage_at": usage.usage_at,
        "amount": usage.amount
    }
    url = reverse('carbon-usage:usage-detail', kwargs={"pk": usage.id})
    response = api_client.put(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "id": usage.id,
        "user": user.id,
        "usage_type": data["usage_type"],
        "usage_at": usage.usage_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "amount": usage.amount,
    }


def test_usage_update_object_with_patch(api_client, user):
    usages = carbon_usage_recipes.base_usage.make(_quantity=5)
    usage = usages[0]
    data = {
        "usage_type": 101,
        "user": user.id
    }
    url = reverse('carbon-usage:usage-detail', kwargs={"pk": usage.id})
    response = api_client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "id": usage.id,
        "user": user.id,
        "usage_type": data["usage_type"],
        "usage_at": usage.usage_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "amount": usage.amount,
    }


def test_usage_delete_object(api_client):
    usages = carbon_usage_recipes.base_usage.make(_quantity=5)
    usage = usages[0]
    url = reverse('carbon-usage:usage-detail', kwargs={"pk": usage.id})

    assert Usage.objects.count() == 5

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Usage.objects.count() == 4


def test_usage_create_object(api_client, user):
    url = reverse('carbon-usage:usage-list')
    data = {
        "user": user.id,
        "usage_type": 100,
        "usage_at": "2020-10-10 10:10",
        "amount": 104.32
    }

    assert Usage.objects.count() == 0

    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    usage = Usage.objects.last()
    assert usage.user_id == data["user"]
    assert usage.usage_type_id == data["usage_type"]
    assert usage.usage_at.strftime("%Y-%m-%d %H:%M") == data["usage_at"]
    assert usage.amount == data["amount"]


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
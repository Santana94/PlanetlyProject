from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status
from . import mommy_recipes as carbon_usage_recipes
from ..models import Usage, UsageTypes

pytestmark = pytest.mark.django_db


def test_usage_is_invalid(client):
    url = reverse('carbon-usage:usage-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_usage_is_valid(api_client):
    url = reverse('carbon-usage:usage-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": []
    }


def test_usage_lists_objects(api_client):
    usages = carbon_usage_recipes.base_usage.make(_quantity=5)
    url = reverse('carbon-usage:usage-list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "count": 5,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": usage.id,
                "user": usage.user.id,
                "usage_type": usage.usage_type.id,
                "usage_at": usage.usage_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "amount": usage.amount,
            }
            for usage in usages
        ]
    }


@pytest.mark.parametrize("ordering_filter, ordering_field", [
    (
        "ordering=user",
        "user"
    ),
    (
        "",
        "id"
    ),
    (
        "ordering=user",
        "user"
    ),
    (
        "ordering=usage_type",
        "usage_type"
    ),
    (
        "ordering=usage_at",
        "usage_at"
    ),
    (
        "ordering=amount",
        "amount"
    ),
])
def test_usage_lists_objects(api_client, ordering_filter, ordering_field):
    usages = carbon_usage_recipes.base_usage.make(_quantity=5)
    url = reverse('carbon-usage:usage-list')
    response = api_client.get(f"{url}?{ordering_filter}")

    assert response.status_code == status.HTTP_200_OK
    expected_usages = [
        {
            "id": usage.id,
            "user": usage.user.id,
            "usage_type": usage.usage_type.id,
            "usage_at": usage.usage_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "amount": usage.amount,
        }
        for usage in usages
    ]
    assert sorted(response.data["results"], key=lambda x: x[ordering_field]) == sorted(
        expected_usages, key=lambda x: x[ordering_field]
    )


@pytest.mark.parametrize("filters, expected_count, extra_data", [
    (
        "",
        10,
        {}
    ),
    (
        "user=42342",
        5,
        {"user_id": 42342}
    ),
    (
        "usage_type=102",
        5,
        {"usage_type_id": 102}
    ),
    (
        "min_usage_at=2021-10-10T15:13",
        5,
        {"usage_at": datetime(2021, 10, 10, 15, 13, 34, 54543)}
    ),
    (
        "max_usage_at=2019-11-10T15:13",
        5,
        {"usage_at": datetime(2019, 10, 10, 15, 13, 34, 54543)}
    ),
    (
        "min_amount=12",
        5,
        {"amount": 15}
    ),
    (
        "max_amount=5",
        5,
        {"amount": 3}
    )
])
def test_usage_with_filters(api_client, filters, expected_count, extra_data):
    carbon_usage_recipes.base_user.make(id=42342)
    usages = carbon_usage_recipes.base_usage.make(_quantity=5, **extra_data)
    not_filtered_usages = carbon_usage_recipes.base_usage.make(
        _quantity=5,
        usage_at=datetime(2020, 10, 10, 15, 13, 34, 54543),
        amount=10
    )
    if not extra_data:
        usages = [*usages, *not_filtered_usages]
    url = reverse('carbon-usage:usage-list')
    response = api_client.get(f"{url}?{filters}")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == expected_count
    assert response.data["results"] == [
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
    assert response.data == {
        "count": 5,
        "next": None,
        "previous": None,
        "results": [
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
    }


def test_usage_types_name_ordering(api_client):
    url = reverse('carbon-usage:usage_types-list')
    response = api_client.get(f"{url}?ordering=name")

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "count": 5,
        "next": None,
        "previous": None,
        "results": [
            {
                "id": 100,
                "name": "electricity",
                "unit": "kwh",
                "factor": 1.5
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
            {
                "id": 101,
                "name": "water",
                "unit": "kg",
                "factor": 26.93
            },
        ]
    }


@pytest.mark.parametrize("filters, expected_data, expected_count", [
    (
        "name=electricity",
        [{
            "id": 100,
            "name": "electricity",
            "unit": "kwh",
            "factor": 1.5
        }],
        1
    ),
    (
        "name=WRONG",
        [],
        0
    ),
    (
        "name=heating",
        [
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
            }
        ],
        3
    ),
    (
        "name=water",
        [{
            "id": 101,
            "name": "water",
            "unit": "kg",
            "factor": 26.93
        }],
        1
    ),
    (
        "unit=kwh",
        [
            {
                "id": 100,
                "name": "electricity",
                "unit": "kwh",
                "factor": 1.5
            },
            {
                "id": 102,
                "name": "heating",
                "unit": "kwh",
                "factor": 3.892
            }
        ],
        2
    ),
    (
        "min_factor=8",
        [
            {
                "id": 101,
                "name": "water",
                "unit": "kg",
                "factor": 26.93
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
            }
        ],
        3
    ),
    (
        "max_factor=8",
        [
            {
                "id": 100,
                "name": "electricity",
                "unit": "kwh",
                "factor": 1.5
            },
            {
                "id": 102,
                "name": "heating",
                "unit": "kwh",
                "factor": 3.892
            },
        ],
        2
    )
])
def test_usage_types_with_filters(api_client, filters, expected_data, expected_count):
    url = reverse('carbon-usage:usage_types-list')
    response = api_client.get(f"{url}?{filters}")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == expected_count
    assert response.data["results"] == expected_data


def test_usage_types_retrieve_object(api_client):
    url = reverse('carbon-usage:usage_types-detail', kwargs={"pk": 101})
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "id": 101,
        "name": "water",
        "unit": "kg",
        "factor": 26.93
    }


def test_usage_types_update_object_with_put(api_client):
    url = reverse('carbon-usage:usage_types-detail', kwargs={"pk": 101})
    data = {
        "name": "water",
        "unit": "g",
        "factor": 6.45
    }
    response = api_client.put(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "id": 101,
        **data
    }


def test_usage_types_update_object_with_patch(api_client):
    url = reverse('carbon-usage:usage_types-detail', kwargs={"pk": 101})
    data = {
        "unit": "g",
        "factor": 6.45
    }
    response = api_client.patch(url, data=data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "id": 101,
        "name": "water",
        **data
    }


def test_usage_types_delete_object(api_client):
    url = reverse('carbon-usage:usage_types-detail', kwargs={"pk": 101})

    assert UsageTypes.objects.count() == 5

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert UsageTypes.objects.count() == 4


def test_usage_types_create_object(api_client):
    url = reverse('carbon-usage:usage_types-list')
    data = {
        "name": "cooling",
        "unit": "m3",
        "factor": 5.34
    }
    assert UsageTypes.objects.count() == 5
    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert UsageTypes.objects.count() == 6
    usage_type = UsageTypes.objects.last()
    assert usage_type.name == data["name"]
    assert usage_type.unit == data["unit"]
    assert usage_type.factor == data["factor"]

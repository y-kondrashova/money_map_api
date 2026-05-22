import pytest
from django.urls import reverse
from rest_framework import status

from apps.category.models import Category


@pytest.mark.django_db
def test_authenticated_user_can_create_category(authenticated_client, user):
    url = reverse("category-list")

    payload = {
        "name": "Test Category",
        "category_type": "INCOME",
    }

    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Category.objects.count() == 1

    category = Category.objects.get(id=response.data["id"])

    assert response.data["name"] == payload["name"]
    assert response.data["category_type"] == payload["category_type"]

    assert category.user == user
    assert category.name == payload["name"]
    assert category.category_type == payload["category_type"]

    assert "id" in response.data
    assert "created_at" in response.data


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_category(api_client):
    url = reverse("category-list")

    payload = {
        "name": "Test Category",
        "category_type": "INCOME",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.data


@pytest.mark.django_db
def test_authenticated_user_sees_only_own_categories(
    authenticated_client, user, another_user
):
    url = reverse("category-list")

    Category.objects.create(name="Salary", user=another_user, category_type="INCOME")
    Category.objects.create(name="Food", user=user, category_type="EXPENSE")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Food"


@pytest.mark.django_db
def test_unauthenticated_user_cannot_list_categories(api_client):
    url = reverse("category-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_authenticated_user_can_retrieve_own_category(authenticated_client, user):
    category = Category.objects.create(
        user=user,
        name="Food",
        category_type="EXPENSE",
    )

    url = reverse("category-detail", kwargs={"pk": category.id})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == category.id
    assert response.data["name"] == category.name


@pytest.mark.django_db
def test_user_cannot_retrieve_another_users_category(
    authenticated_client,
    another_user,
):
    category = Category.objects.create(
        user=another_user,
        name="Salary",
        category_type="INCOME",
    )

    url = reverse("category-detail", kwargs={"pk": category.id})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_authenticated_user_can_update_own_category(authenticated_client, user):
    category = Category.objects.create(
        user=user,
        name="Old Name",
        category_type="EXPENSE",
    )

    url = reverse("category-detail", kwargs={"pk": category.id})

    payload = {
        "name": "New Name",
    }

    response = authenticated_client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK

    category.refresh_from_db()

    assert category.name == "New Name"
    assert response.data["name"] == "New Name"


@pytest.mark.django_db
def test_user_cannot_update_another_users_category(
    authenticated_client,
    another_user,
):
    category = Category.objects.create(
        user=another_user,
        name="Salary",
        category_type="INCOME",
    )

    url = reverse("category-detail", kwargs={"pk": category.id})
    response = authenticated_client.patch(url, {"name": "Changed"}, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_cannot_create_duplicate_category(authenticated_client, user):
    Category.objects.create(
        user=user,
        name="Food",
        category_type="EXPENSE",
    )

    url = reverse("category-list")

    payload = {
        "name": "Food",
        "category_type": "EXPENSE",
    }
    response = authenticated_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_user_can_soft_delete_own_category(authenticated_client, user):
    category = Category.objects.create(
        user=user,
        name="Food",
        category_type="EXPENSE",
    )
    url = reverse("category-detail", kwargs={"pk": category.id})

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_deleted_category_is_not_returned_in_list(authenticated_client, user):
    category = Category.objects.create(
        user=user,
        name="Food",
        category_type="EXPENSE",
    )
    category.delete()
    url = reverse("category-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
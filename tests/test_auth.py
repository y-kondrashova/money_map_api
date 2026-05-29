import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_user_can_register(api_client):
    url = reverse("register")

    payload = {
        "email": "test@example.com",
        "password": "strongpassword123",
        "password_confirm": "strongpassword123",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == payload["email"]
    assert "access" in response.data
    assert "refresh" in response.data
    assert "password" not in response.data


@pytest.mark.django_db
def test_authenticated_user_can_get_profile(authenticated_client, user):
    url = reverse("profile")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == user.id
    assert response.data["email"] == user.email
    assert response.data["first_name"] == user.first_name
    assert response.data["last_name"] == user.last_name

    assert "created_at" in response.data
    assert "access" not in response.data
    assert "password" not in response.data


@pytest.mark.django_db
def test_authenticated_user_can_update_profile(authenticated_client, user):
    url = reverse("profile")

    payload = {"first_name": "John", "last_name": "Doe"}

    response = authenticated_client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.first_name == payload["first_name"]
    assert user.last_name == payload["last_name"]
    assert response.data["first_name"] == payload["first_name"]
    assert response.data["last_name"] == payload["last_name"]


@pytest.mark.django_db
def test_unauthenticated_user_cannot_get_profile(api_client):
    url = reverse("profile")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in response.data


@pytest.mark.django_db
def test_user_cannot_update_email(authenticated_client, user):
    url = reverse("profile")

    old_email = user.email
    payload = {"email": "new.good@email.com"}

    response = authenticated_client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.email == old_email
    assert response.data["email"] == old_email

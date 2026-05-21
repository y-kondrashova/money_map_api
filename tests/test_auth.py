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
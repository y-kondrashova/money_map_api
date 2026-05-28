import pytest
from django.urls import reverse
from rest_framework import status

from apps.wallets.models import Wallet


@pytest.mark.django_db
def test_authenticated_user_can_create_wallet(authenticated_client, user):
    url = reverse("wallet-list")

    payload = {"name": "Cash"}
    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Wallet.objects.count() == 1

    wallet = Wallet.objects.get(id=response.data["id"])

    assert response.data["name"] == payload["name"]
    assert wallet.user == user
    assert wallet.name == payload["name"]

    assert "id" in response.data
    assert "created_at" in response.data


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_wallet(api_client):
    url = reverse("wallet-list")

    payload = {"name": "Cash"}
    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.data


@pytest.mark.django_db
def test_user_sees_only_own_wallets(authenticated_client, user, another_user):
    url = reverse("wallet-list")

    Wallet.objects.create(user=another_user, name="Another Wallet")
    Wallet.objects.create(user=user, name="My Wallet")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "My Wallet"


@pytest.mark.django_db
def test_authenticated_user_can_retrieve_own_wallet(authenticated_client, user):
    wallet = Wallet.objects.create(user=user, name="Cash")
    url = reverse("wallet-detail", kwargs={"pk": wallet.id})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == wallet.id
    assert response.data["name"] == wallet.name


@pytest.mark.django_db
def test_user_cannot_retrieve_another_users_wallet(authenticated_client, another_user):
    wallet = Wallet.objects.create(user=another_user, name="Another Wallet")
    url = reverse("wallet-detail", kwargs={"pk": wallet.id})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_can_update_own_wallet(authenticated_client, user):
    wallet = Wallet.objects.create(user=user, name="Cash")

    url = reverse("wallet-detail", kwargs={"pk": wallet.id})

    payload = {"name": "Card"}

    response = authenticated_client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK

    wallet.refresh_from_db()

    assert wallet.name == "Card"
    assert response.data["name"] == "Card"


@pytest.mark.django_db
def test_user_cannot_update_another_users_wallet(authenticated_client, another_user):
    wallet = Wallet.objects.create(user=another_user, name="Another Wallet")

    url = reverse("wallet-detail", kwargs={"pk": wallet.id})
    response = authenticated_client.patch(url, {"name": "Card"}, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_cannot_create_duplicate_wallet(authenticated_client, user):
    Wallet.objects.create(user=user, name="Cash")
    url = reverse("wallet-list")
    payload = {"name": "Cash"}

    response = authenticated_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert Wallet.objects.count() == 1


@pytest.mark.django_db
def test_user_can_soft_delete_own_wallet(authenticated_client, user):
    wallet = Wallet.objects.create(user=user, name="Cash")
    url = reverse("wallet-detail", kwargs={"pk": wallet.id})

    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_deleted_wallet_is_not_returned_in_list(authenticated_client, user):
    wallet = Wallet.objects.create(user=user, name="Cash")
    wallet.delete()
    url = reverse("wallet-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0

from datetime import date
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status

from apps.transactions.models import Transaction
from apps.wallets.models import Wallet
from apps.category.models import Category


@pytest.mark.django_db
def test_authenticated_user_can_create_transaction(
    authenticated_client,
    user,
    user_wallet,
    user_category,
):
    url = reverse("transaction-list")

    payload = {
        "category": user_category.id,
        "wallet": user_wallet.id,
        "amount": "10.00",
        "date": "2026-05-01",
    }

    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Transaction.objects.count() == 1

    transaction = Transaction.objects.get(id=response.data["id"])

    assert transaction.category == user_category
    assert transaction.wallet == user_wallet
    assert transaction.user == user
    assert transaction.amount == Decimal("10.00")
    assert transaction.date == date(2026, 5, 1)

    assert response.data["category"] == user_category.id
    assert response.data["wallet"] == user_wallet.id
    assert response.data["amount"] == "10.00"
    assert response.data["date"] == payload["date"]
    assert "id" in response.data
    assert "created_at" in response.data
    assert "updated_at" in response.data


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_transaction(
    api_client,
    user_wallet,
    user_category,
):
    url = reverse("transaction-list")

    payload = {
        "category": user_category.id,
        "wallet": user_wallet.id,
        "amount": "10.00",
        "date": "2026-05-01",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_authenticated_user_sees_only_own_transactions(
    authenticated_client,
    user,
    another_user,
    user_wallet,
    user_category,
):
    another_user_wallet = Wallet.objects.create(
        user=another_user,
        name="Another Cash",
        currency="USD",
    )
    another_user_category = Category.objects.create(
        user=another_user,
        name="Another Food",
        category_type="EXPENSE",
    )

    Transaction.objects.create(
        user=user,
        wallet=user_wallet,
        category=user_category,
        amount=Decimal("10.00"),
        date=date(2026, 5, 1),
    )
    Transaction.objects.create(
        user=another_user,
        wallet=another_user_wallet,
        category=another_user_category,
        amount=Decimal("50.00"),
        date=date(2026, 5, 2),
    )

    url = reverse("transaction-list")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["amount"] == "10.00"


@pytest.mark.django_db
def test_user_can_retrieve_own_transaction(
    authenticated_client,
    user,
    user_wallet,
    user_category,
):
    transaction = Transaction.objects.create(
        user=user,
        wallet=user_wallet,
        category=user_category,
        amount=Decimal("10.00"),
        date=date(2026, 5, 1),
    )

    url = reverse("transaction-detail", kwargs={"pk": transaction.id})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == transaction.id
    assert response.data["amount"] == "10.00"


@pytest.mark.django_db
def test_user_cannot_retrieve_another_users_transaction(
    authenticated_client,
    another_user,
):
    another_user_wallet = Wallet.objects.create(
        user=another_user,
        name="Another Cash",
        currency="USD",
        initial_balance=Decimal("0.00"),
    )
    another_user_category = Category.objects.create(
        user=another_user,
        name="Another Food",
        category_type="EXPENSE",
    )
    transaction = Transaction.objects.create(
        user=another_user,
        wallet=another_user_wallet,
        category=another_user_category,
        amount=Decimal("50.00"),
        date=date(2026, 5, 2),
    )

    url = reverse("transaction-detail", kwargs={"pk": transaction.id})

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_cannot_create_transaction_with_another_users_wallet(
    authenticated_client,
    another_user,
    user_category,
):
    another_user_wallet = Wallet.objects.create(
        user=another_user,
        name="Another Cash",
        currency="USD",
        initial_balance=Decimal("0.00"),
    )

    url = reverse("transaction-list")

    payload = {
        "category": user_category.id,
        "wallet": another_user_wallet.id,
        "amount": "10.00",
        "date": "2026-05-01",
    }

    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Transaction.objects.count() == 0
    assert "wallet" in response.data


@pytest.mark.django_db
def test_user_cannot_create_transaction_with_another_users_category(
    authenticated_client,
    another_user,
    user_wallet,
):
    another_user_category = Category.objects.create(
        user=another_user,
        name="Another Food",
        category_type="EXPENSE",
    )

    url = reverse("transaction-list")

    payload = {
        "category": another_user_category.id,
        "wallet": user_wallet.id,
        "amount": "10.00",
        "date": "2026-05-01",
    }

    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Transaction.objects.count() == 0
    assert "category" in response.data


@pytest.mark.django_db
def test_user_cannot_create_transaction_with_zero_amount(
    authenticated_client,
    user_wallet,
    user_category,
):
    url = reverse("transaction-list")

    payload = {
        "category": user_category.id,
        "wallet": user_wallet.id,
        "amount": "0.00",
        "date": "2026-05-01",
    }

    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Transaction.objects.count() == 0
    assert "amount" in response.data


@pytest.mark.django_db
def test_user_cannot_create_transaction_with_negative_amount(
    authenticated_client,
    user_wallet,
    user_category,
):
    url = reverse("transaction-list")

    payload = {
        "category": user_category.id,
        "wallet": user_wallet.id,
        "amount": "-10.00",
        "date": "2026-05-01",
    }

    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Transaction.objects.count() == 0
    assert "amount" in response.data


@pytest.mark.django_db
def test_user_can_update_own_transaction(
    authenticated_client,
    user,
    user_wallet,
    user_category,
):
    transaction = Transaction.objects.create(
        user=user,
        wallet=user_wallet,
        category=user_category,
        amount=Decimal("10.00"),
        date=date(2026, 5, 1),
    )

    url = reverse("transaction-detail", kwargs={"pk": transaction.id})

    payload = {
        "amount": "25.00",
        "title": "Updated transaction",
    }

    response = authenticated_client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK

    transaction.refresh_from_db()

    assert transaction.amount == Decimal("25.00")
    assert transaction.title == "Updated transaction"
    assert response.data["amount"] == "25.00"
    assert response.data["title"] == "Updated transaction"


@pytest.mark.django_db
def test_user_cannot_update_another_users_transaction(
    authenticated_client,
    another_user,
):
    another_user_wallet = Wallet.objects.create(
        user=another_user,
        name="Another Cash",
        currency="USD",
        initial_balance=Decimal("0.00"),
    )
    another_user_category = Category.objects.create(
        user=another_user,
        name="Another Food",
        category_type="EXPENSE",
    )
    transaction = Transaction.objects.create(
        user=another_user,
        wallet=another_user_wallet,
        category=another_user_category,
        amount=Decimal("50.00"),
        date=date(2026, 5, 2),
    )

    url = reverse("transaction-detail", kwargs={"pk": transaction.id})

    response = authenticated_client.patch(
        url,
        {"amount": "100.00"},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    transaction.refresh_from_db()

    assert transaction.amount == Decimal("50.00")


@pytest.mark.django_db
def test_user_can_delete_own_transaction(
    authenticated_client,
    user,
    user_wallet,
    user_category,
):
    transaction = Transaction.objects.create(
        user=user,
        wallet=user_wallet,
        category=user_category,
        amount=Decimal("10.00"),
        date=date(2026, 5, 1),
    )

    url = reverse("transaction-detail", kwargs={"pk": transaction.id})

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_user_cannot_delete_another_users_transaction(
    authenticated_client,
    another_user,
):
    another_user_wallet = Wallet.objects.create(
        user=another_user,
        name="Another Cash",
        currency="USD",
        initial_balance=Decimal("0.00"),
    )
    another_user_category = Category.objects.create(
        user=another_user,
        name="Another Food",
        category_type="EXPENSE",
    )
    transaction = Transaction.objects.create(
        user=another_user,
        wallet=another_user_wallet,
        category=another_user_category,
        amount=Decimal("50.00"),
        date=date(2026, 5, 2),
    )

    url = reverse("transaction-detail", kwargs={"pk": transaction.id})

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Transaction.objects.count() == 1

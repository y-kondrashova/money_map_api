import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.category.models import Category
from apps.wallets.models import Wallet

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        email="test@example.com", password="strongpassword123"
    )


@pytest.fixture
def another_user():
    return User.objects.create_user(
        email="test2@example.com", password="strongpassword2123"
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user_category(user):
    return Category.objects.create(user=user, name="Food", category_type="EXPENSE")


@pytest.fixture
def another_user_category(another_user):
    return Category.objects.create(
        user=another_user, name="Restaurants", category_type="EXPENSE"
    )


@pytest.fixture
def user_wallet(user):
    return Wallet.objects.create(user=user, name="Cash", initial_balance=1000)

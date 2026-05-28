import pytest
from django.urls import reverse
from rest_framework import status

from apps.budgets.models import Budget
from apps.category.models import Category


@pytest.mark.django_db
def test_authenticated_user_can_create_budget(
    authenticated_client, user, user_category
):
    url = reverse("budget-list")

    payload = {
        "name": "Test Budget",
        "limit_amount": 600,
        "category": user_category.id,
        "start_date": "2026-05-01",
        "end_date": "2026-05-31",
    }

    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Budget.objects.count() == 1


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_budget(api_client, user_category):
    url = reverse("budget-list")

    payload = {
        "name": "Test Budget",
        "limit_amount": 600,
        "category": user_category.id,
        "start_date": "2026-05-01",
        "end_date": "2026-05-31",
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Budget.objects.count() == 0


@pytest.mark.django_db
def test_user_sees_only_own_budgets(
    authenticated_client, user, another_user, user_category, another_user_category
):
    url = reverse("budget-list")
    Budget.objects.create(
        user=another_user,
        name="Another Budget",
        limit_amount=600,
        category=another_user_category,
        start_date="2026-05-01",
        end_date="2026-05-31",
    )
    Budget.objects.create(
        user=user,
        name="My Budget",
        limit_amount=600,
        category=user_category,
        start_date="2026-05-01",
        end_date="2026-05-31",
    )
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "My Budget"


@pytest.mark.django_db
def test_authenticated_user_can_retrieve_own_budget(
    authenticated_client, user, user_category
):
    budget = Budget.objects.create(
        user=user,
        name="Another Budget",
        limit_amount=600,
        category=user_category,
        start_date="2026-05-01",
        end_date="2026-05-31",
    )

    url = reverse("budget-detail", kwargs={"pk": budget.id})
    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == budget.id
    assert response.data["name"] == budget.name


@pytest.mark.django_db
def test_user_cannot_retrieve_another_users_budget(
    authenticated_client, another_user, another_user_category
):
    budget = Budget.objects.create(
        user=another_user,
        name="Another Budget",
        limit_amount=600,
        category=another_user_category,
        start_date="2026-05-01",
        end_date="2026-05-31",
    )

    url = reverse("budget-detail", kwargs={"pk": budget.id})

    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_can_update_own_budget(authenticated_client, user, user_category):
    budget = Budget.objects.create(
        user=user,
        name="Another Budget",
        limit_amount=600,
        category=user_category,
        start_date="2026-05-01",
        end_date="2026-05-31",
    )

    url = reverse("budget-detail", kwargs={"pk": budget.id})
    payload = {"name": "Food Budget"}

    response = authenticated_client.patch(url, payload, format="json")

    assert response.status_code == status.HTTP_200_OK

    budget.refresh_from_db()

    assert budget.name == "Food Budget"
    assert response.data["name"] == "Food Budget"


@pytest.mark.django_db
def test_user_cannot_update_another_users_budget(
    authenticated_client, another_user, another_user_category
):
    budget = Budget.objects.create(
        user=another_user,
        name="Another Budget",
        limit_amount=600,
        category=another_user_category,
        start_date="2026-05-01",
        end_date="2026-05-31",
    )
    url = reverse("budget-detail", kwargs={"pk": budget.id})
    payload = {"name": "Food Budget"}
    response = authenticated_client.patch(url, payload, format="json")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_cannot_create_duplicate_budget(authenticated_client, user, user_category):
    Budget.objects.create(
        user=user,
        name="Food Budget",
        limit_amount=600,
        category=user_category,
        start_date="2026-05-01",
        end_date="2026-05-31",
    )

    url = reverse("budget-list")
    payload = {
        "name": "Food Budget",
        "limit_amount": 600,
        "category": user_category.id,
        "start_date": "2026-05-01",
        "end_date": "2026-05-31",
    }
    response = authenticated_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Budget.objects.count() == 1


@pytest.mark.django_db
def test_user_cannot_create_budget_for_income_category(authenticated_client, user):
    url = reverse("budget-list")
    category = Category.objects.create(
        user=user,
        name="Salary",
        category_type="INCOME",
    )
    payload = {
        "name": "Food Budget",
        "limit_amount": 600,
        "category": category.id,
        "start_date": "2026-05-01",
        "end_date": "2026-05-31",
    }
    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Budget.objects.count() == 0


@pytest.mark.django_db
def test_user_can_soft_delete_own_budget(authenticated_client, user, user_category):
    budget = Budget.objects.create(
        user=user,
        name="Food Budget",
        limit_amount=600,
        category=user_category,
        start_date="2026-05-01",
        end_date="2026-05-31",
    )
    url = reverse("budget-detail", kwargs={"pk": budget.id})

    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_deleted_budget_is_not_returned_in_list(
    authenticated_client, user, user_category
):
    budget = Budget.objects.create(
        user=user,
        name="Food Budget",
        limit_amount=600,
        category=user_category,
        start_date="2026-05-01",
        end_date="2026-05-31",
    )
    budget.delete()

    url = reverse("budget-list")

    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_budget_cannot_have_end_date_before_start_date(
    authenticated_client, user, user_category
):
    url = reverse("budget-list")
    payload = {
        "name": "Food Budget",
        "limit_amount": 600,
        "category": user_category.id,
        "start_date": "2026-05-31",
        "end_date": "2026-05-01",
    }
    response = authenticated_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Budget.objects.count() == 0

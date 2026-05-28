from rest_framework import serializers
from apps.budgets.models import Budget
from decimal import Decimal

from apps.budgets.services import calculate_budget_progress


class BudgetSerializer(serializers.ModelSerializer):
    spent_amount = serializers.SerializerMethodField()
    remaining_amount = serializers.SerializerMethodField()
    used_percent = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Budget
        fields = [
            "id",
            "name",
            "category",
            "limit_amount",
            "spent_amount",
            "remaining_amount",
            "used_percent",
            "status",
            "period",
            "start_date",
            "end_date",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_active", "created_at", "updated_at"]

    @staticmethod
    def get_spent_amount(obj):
        return calculate_budget_progress(obj)["spent_amount"]

    @staticmethod
    def get_remaining_amount(obj):
        return calculate_budget_progress(obj)["remaining_amount"]

    @staticmethod
    def get_used_percent(obj):
        return calculate_budget_progress(obj)["used_percent"]

    @staticmethod
    def get_status(obj):
        return calculate_budget_progress(obj)["status"]

    @staticmethod
    def validate_limit_amount(value):
        if value < Decimal("0.01"):
            raise serializers.ValidationError("Limit amount must be greater than 0.")
        return value

    def validate(self, attrs):

        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Autheticated user is required.")

        user = request.user

        category = attrs.get("category", getattr(self.instance, "category", None))
        start_date = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end_date = attrs.get("end_date", getattr(self.instance, "end_date", None))

        budget_exists = Budget.objects.filter(
            user=user,
            category=category,
            start_date=start_date,
            end_date=end_date,
        )

        if category and category.user != user:
            raise serializers.ValidationError(
                {"category": "This category does not belong to you."}
            )

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                {"end_date": "End date cannot be earlier than start date."}
            )

        if self.instance:
            budget_exists = budget_exists.exclude(pk=self.instance.pk)

        if budget_exists.exists():
            raise serializers.ValidationError(
                {"category": "Budget for this category already exists."}
            )

        if category.category_type != "EXPENSE":
            raise serializers.ValidationError(
                {"category": "Budget can be created only for expense categories."}
            )

        return attrs

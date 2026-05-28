from rest_framework import serializers
from apps.transactions.models import Transaction
from decimal import Decimal


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "category",
            "wallet",
            "title",
            "amount",
            "transaction_type",
            "date",
            "note",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "transaction_type", "created_at", "updated_at"]

    @staticmethod
    def validate_amount(value):
        if value < Decimal("0.01"):
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    @staticmethod
    def validate_title(value):
        return value.strip()

    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Authenticated user is required.")

        user = request.user
        wallet = attrs.get("wallet", getattr(self.instance, "wallet", None))
        category = attrs.get("category", getattr(self.instance, "category", None))

        if wallet and wallet.user != user:
            raise serializers.ValidationError(
                {"wallet": "This wallet does not belong to you."}
            )

        if wallet and not wallet.is_active:
            raise serializers.ValidationError({"wallet": "This wallet is inactive."})

        if category and category.user != user:
            raise serializers.ValidationError(
                {"category": "This category does not belong to you."}
            )

        if category and not category.is_active:
            raise serializers.ValidationError(
                {"category": "This category is inactive."}
            )

        return attrs

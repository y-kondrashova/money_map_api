from rest_framework import serializers
from apps.wallets.models import Wallet
from decimal import Decimal


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            "id",
            "name",
            "currency",
            "initial_balance",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "is_active", "created_at", "updated_at"]

    @staticmethod
    def validate_name(value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Wallet name cannot be empty.")
        return value

    @staticmethod
    def validate_currency(value):
        value = value.strip().upper()

        if len(value) != 3:
            raise serializers.ValidationError("Currency must be 3 characters long.")
        if not value.isalpha():
            raise serializers.ValidationError("Currency must contain only letters.")
        return value

    @staticmethod
    def validate_initial_balance(value):
        if value < Decimal("0.00"):
            raise serializers.ValidationError("Initial balance cannot be negative.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Autheticated user is required.")

        user = request.user
        name = attrs.get("name", getattr(self.instance, "name", None))

        wallet_exists = Wallet.objects.filter(user=user, name__iexact=name)

        if self.instance:
            wallet_exists = wallet_exists.exclude(pk=self.instance.pk)

        if wallet_exists.exists():
            raise serializers.ValidationError(
                {"name": "Wallet with this name already exists."}
            )

        return attrs

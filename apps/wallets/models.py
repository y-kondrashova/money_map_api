from django.db import models

from config import settings


class Wallet(models.Model):
    """
    Represents user's money storage/source, such as cash, bank card, savings account, etc.
    """

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallets"
    )
    currency = models.CharField(max_length=3, default="USD")
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "wallets"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(fields=["name", "user"], name="unique_wallet"),
        ]

    def __str__(self):
        return f"{self.name} ({self.currency})"

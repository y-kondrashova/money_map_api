from django.db import models
from django.conf import settings


class Transaction(models.Model):
    """Represents user's financial operation."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey("category.Category", on_delete=models.PROTECT)
    wallet = models.ForeignKey("wallets.Wallet", on_delete=models.PROTECT)
    title = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def transaction_type(self):
        return self.category.category_type

    class Meta:
        db_table = "transactions"
        ordering = (
            "-date",
            "-created_at",
        )

    def __str__(self):
        return f"{self.title} - {self.amount} {self.wallet.currency}, Category({self.category.name})"

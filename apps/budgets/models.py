from django.db import models
from django.conf import settings


class Budget(models.Model):
    """Represents user's spending limit for a specific category and period."""

    class Period(models.TextChoices):
        WEEKLY = "WEEKLY", "Weekly"
        MONTHLY = "MONTHLY", "Monthly"
        YEARLY = "YEARLY", "Yearly"
        CUSTOM = "CUSTOM", "Custom"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="budgets",
    )
    category = models.ForeignKey(
        "category.Category",
        on_delete=models.PROTECT,
        related_name="budgets",
    )
    name = models.CharField(max_length=100)
    limit_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    period = models.CharField(
        max_length=10, choices=Period.choices, default=Period.MONTHLY
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "budgets"
        ordering = (
            "-start_date",
            "name",
        )
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category", "start_date", "end_date"],
                name="unique_budget",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.category}) - {self.limit_amount}"

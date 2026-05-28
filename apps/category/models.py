from django.db import models

from config import settings


class Category(models.Model):
    class CategoryType(models.TextChoices):
        INCOME = "INCOME", "Income"
        EXPENSE = "EXPENSE", "Expense"

    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    category_type = models.CharField(max_length=10, choices=CategoryType.choices)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=["name", "user", "category_type"],
                name="unique_category",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.category_type})"

from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    ordering = ("-date",)
    list_display = (
        "id",
        "category",
        "wallet",
        "title",
        "date",
        "amount",
        "note",
        "transaction_type",
        "created_at",
        "updated_at",
        "user",
    )
    list_display_links = ("id", "title")
    list_filter = ("category__category_type", "date", "created_at")
    search_fields = (
        "category__name",
        "wallet__name",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = ("id", "transaction_type", "created_at", "updated_at")
    date_hierarchy = "date"
    list_per_page = 25
    list_select_related = ("user", "category", "wallet")

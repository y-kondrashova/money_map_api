from django.contrib import admin
from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = (
        "id",
        "name",
        "user",
        "currency",
        "initial_balance",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "name")
    list_editable = ("is_active",)
    list_filter = ("currency", "is_active", "created_at")
    search_fields = ("name", "user__email", "user__first_name", "user__last_name")
    readonly_fields = ("id", "created_at", "updated_at")
    date_hierarchy = "created_at"
    list_per_page = 25
    list_select_related = ("user",)

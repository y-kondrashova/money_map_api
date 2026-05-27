from django.contrib import admin
from .models import Budget

admin.site.register(Budget)


class BudgetAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = (
        "id",
        "name",
        "category",
        "limit_amount",
        "period",
        "start_date",
        "end_date",
        "is_active",
        "created_at",
        "updated_at",
        "user",
    )
    list_display_links = ("id", "name")
    list_editable = ("is_active",)
    list_filter = ("period", "is_active", "created_at")
    search_fields = ("name", "user__email", "user__first_name", "user__last_name")
    readonly_fields = ("id", "created_at", "updated_at")
    date_hierarchy = "created_at"
    list_per_page = 25
    list_select_related = ("user",)

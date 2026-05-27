from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ("name",)
    list_display = (
        "id",
        "name",
        "category_type",
        "user",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_display_links = ("id", "name")
    list_editable = ("is_active",)
    list_filter = ("category_type", "is_active", "created_at")
    search_fields = ("name", "user__email", "user__first_name", "user__last_name")
    readonly_fields = ("id", "created_at", "updated_at")
    date_hierarchy = "created_at"
    list_per_page = 25
    list_select_related = ("user",)

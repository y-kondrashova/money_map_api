"""URL configuration for config project."""

from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import home, api_root

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", api_root, name="api-root"),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(permission_classes=[AllowAny]),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema", permission_classes=[AllowAny]
        ),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema", permission_classes=[AllowAny]),
        name="redoc",
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/categories/", include("apps.category.urls")),
    path("api/wallets/", include("apps.wallets.urls")),
    path("api/budgets/", include("apps.budgets.urls")),
    path("api/transactions/", include("apps.transactions.urls")),
]

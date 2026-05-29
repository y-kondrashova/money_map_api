from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response


def home(request):
    links = [
        {
            "title": "Swagger Docs",
            "description": "Interactive API documentation with Swagger UI.",
            "url": "/api/docs/",
        },
        {
            "title": "ReDoc",
            "description": "Alternative API documentation view.",
            "url": "/api/redoc/",
        },
        {
            "title": "OpenAPI Schema",
            "description": "Raw OpenAPI schema for the API.",
            "url": "/api/schema/",
        },
        {
            "title": "API Root",
            "description": "Main API overview page.",
            "url": "/api/",
        },
        {
            "title": "Register",
            "description": "Create a new user account.",
            "url": "/api/auth/register/",
        },
        {
            "title": "DRF Login",
            "description": "Login to use the browsable API.",
            "url": "/api-auth/login/",
        },
        {
            "title": "Token",
            "description": "Get JWT access and refresh tokens.",
            "url": "/api/auth/token/",
        },
        {
            "title": "Token Refresh",
            "description": "Refresh JWT access token.",
            "url": "/api/auth/token/refresh/",
        },
        {
            "title": "Categories",
            "description": "Manage income and expense categories.",
            "url": "/api/categories/",
        },
        {
            "title": "Wallets",
            "description": "Manage user wallets and balances.",
            "url": "/api/wallets/",
        },
        {
            "title": "Budgets",
            "description": "Manage budgets and spending limits.",
            "url": "/api/budgets/",
        },
        {
            "title": "Transactions",
            "description": "Create and manage financial transactions.",
            "url": "/api/transactions/",
        },
        {
            "title": "Admin Panel",
            "description": "Django admin panel.",
            "url": "/admin/",
        },
    ]

    return render(request, "home.html", {"links": links})


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "project": "MoneyMap API",
            "status": "Backend MVP in development",
            "description": "Personal finance backend API for wallets, categories, transactions and budgets.",
            "authentication": {
                "register": request.build_absolute_uri("/api/auth/register/"),
                "token": request.build_absolute_uri("/api/auth/token/"),
                "token_refresh": request.build_absolute_uri("/api/auth/token/refresh/"),
                "drf_login": request.build_absolute_uri("/api-auth/login/?next=/api/"),
            },
            "endpoints": {
                "categories": request.build_absolute_uri("/api/categories/"),
                "wallets": request.build_absolute_uri("/api/wallets/"),
                "budgets": request.build_absolute_uri("/api/budgets/"),
                "transactions": request.build_absolute_uri("/api/transactions/"),
            },
            "admin": request.build_absolute_uri("/admin/"),
        }
    )

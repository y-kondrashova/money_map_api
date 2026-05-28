from decimal import Decimal

from django.db.models import Q, Sum

from apps.transactions.models import Transaction


def calculate_wallet_balance(wallet):
    totals = Transaction.objects.filter(
        user=wallet.user,
        wallet=wallet,
    ).aggregate(
        income_total=Sum(
            "amount",
            filter=Q(category__category_type="INCOME"),
        ),
        expense_total=Sum(
            "amount",
            filter=Q(category__category_type="EXPENSE"),
        ),
    )

    income_total = totals["income_total"] or Decimal("0.00")
    expense_total = totals["expense_total"] or Decimal("0.00")

    return wallet.initial_balance + income_total - expense_total

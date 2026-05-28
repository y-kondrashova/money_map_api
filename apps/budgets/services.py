from decimal import Decimal

from django.db.models import Sum

from apps.transactions.models import Transaction


def calculate_budget_progress(budget):
    spent_amount = Transaction.objects.filter(
        user=budget.user,
        category=budget.category,
        category__category_type="EXPENSE",
        date__gte=budget.start_date,
        date__lte=budget.end_date,
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    remaining_amount = budget.limit_amount - spent_amount

    if budget.limit_amount > 0:
        used_percent = spent_amount / budget.limit_amount * Decimal("100")
    else:
        used_percent = Decimal("0.00")

    if spent_amount > budget.limit_amount:
        status = "exceeded"
    elif used_percent >= 80:
        status = "near_limit"
    else:
        status = "within_limit"

    return {
        "limit_amount": budget.limit_amount,
        "spent_amount": spent_amount,
        "remaining_amount": remaining_amount,
        "used_percent": round(used_percent, 2),
        "status": status,
    }

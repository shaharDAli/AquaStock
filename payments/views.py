from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from sales.models import Sale
from refill.models import Refill
from .models import Payment


def payment_add(request, sale_id=None, refill_id=None):

    sale = None
    refill = None

    if sale_id:
        sale = get_object_or_404(Sale, id=sale_id)

    if refill_id:
        refill = get_object_or_404(Refill, id=refill_id)

    error = None

    if request.method == "POST":

        amount = request.POST.get("amount")

        try:
            Payment.objects.create(
                sale=sale,
                refill=refill,
                amount=amount
            )
            return redirect("sales_list")

        except ValidationError as e:
            error = e

    return render(
        request,
        "payments/payment_add.html",
        {
            "sale": sale,
            "refill": refill,
            "error": error
        }
    )

def payment_history(request, sale_id):

    sale = get_object_or_404(Sale, id=sale_id)

    payments = Payment.objects.filter(sale=sale).order_by("-paid_at")

    total_paid = sum(p.amount for p in payments)

    balance = sale.total_amount - total_paid

    return render(
        request,
        "payments/payment_history.html",
        {
            "sale": sale,
            "payments": payments,
            "total_paid": total_paid,
            "balance": balance
        }
    )
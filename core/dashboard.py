from django.utils import timezone
from django.db.models import F, FloatField, Sum
from production.models import Production
from sales.models import Sale
from refill.models import Refill
from products.models import LitreMaster


def dashboard_summary():
    """
    Returns dynamic summary for AquaStock Dashboard
    - Today production
    - Today sales
    - Today refill revenue
    - Walk-in revenue
    - Pending (credit) revenue
    - Current stock per litre
    """

    today = timezone.now().date()

    # ---------------------------
    # Production today
    # ---------------------------
    production_total = Production.objects.filter(
        created_at__date=today
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # ---------------------------
    # Sales today
    # ---------------------------
    sales_total = Sale.objects.filter(
        created_at__date=today
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0

    # ---------------------------
    # Refill revenue today
    # ---------------------------
    refill_qs = Refill.objects.filter(created_at__date=today)
    refill_revenue = refill_qs.aggregate(
        revenue=Sum(F('unit_price') * F('quantity'), output_field=FloatField())
    )['revenue'] or 0

    # ---------------------------
    # Walk-in revenue today
    # ---------------------------
    walkin_sales = Sale.objects.filter(
        created_at__date=today,
        customer_type=Sale.WALK_IN
    ).aggregate(
        revenue=Sum(F('unit_price') * F('quantity'), output_field=FloatField())
    )['revenue'] or 0

    walkin_refill = Refill.objects.filter(
        created_at__date=today,
        customer_type=Refill.WALK_IN
    ).aggregate(
        revenue=Sum(F('unit_price') * F('quantity'), output_field=FloatField())
    )['revenue'] or 0

    walkin_total = walkin_sales + walkin_refill

    # ---------------------------
    # Pending / Credit revenue today
    # ---------------------------
    pending_total = 0

    provider_sales = Sale.objects.filter(
        created_at__date=today,
        customer_type=Sale.PROVIDER
    )
    provider_refills = Refill.objects.filter(
        created_at__date=today,
        customer_type=Refill.PROVIDER
    )

    for s in provider_sales:
        total_paid = sum(p.amount for p in s.payment_set.all())
        pending_total += (s.total_amount - total_paid)

    for r in provider_refills:
        total_paid = sum(p.amount for p in r.payment_set.all())
        pending_total += (r.total_amount - total_paid)

    # ---------------------------
    # Current stock summary per litre
    # ---------------------------
    stock_summary = {litre.name: litre.current_stock for litre in LitreMaster.objects.all()}

    # ---------------------------
    # Return dictionary
    # ---------------------------
    return {
        "today_production": production_total,
        "today_sales": sales_total,
        "refill_revenue": refill_revenue,
        "walkin_total": walkin_total,
        "pending_total": pending_total,
        "stock_summary": stock_summary
    }
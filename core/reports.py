from django.db.models import Sum, F, FloatField
from production.models import Production
from sales.models import Sale
from refill.models import Refill
from products.models import LitreMaster
from payments.models import Payment

def production_report(start_date=None, end_date=None, litre=None):
    qs = Production.objects.all()
    if start_date:
        qs = qs.filter(created_at__date__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__date__lte=end_date)
    if litre:
        qs = qs.filter(litre__id=litre.id)
    return qs

def sales_report(start_date=None, end_date=None, litre=None, party=None):
    qs = Sale.objects.all()
    if start_date:
        qs = qs.filter(created_at__date__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__date__lte=end_date)
    if litre:
        qs = qs.filter(litre__id=litre.id)
    if party:
        qs = qs.filter(party=party)
    return qs

def refill_report(start_date=None, end_date=None, party=None):
    qs = Refill.objects.all()
    if start_date:
        qs = qs.filter(created_at__date__gte=start_date)
    if end_date:
        qs = qs.filter(created_at__date__lte=end_date)
    if party:
        qs = qs.filter(party=party)
    return qs

def pending_report(party=None):
    from django.db.models import Q
    sales = Sale.objects.all()
    refills = Refill.objects.all()
    if party:
        sales = sales.filter(party=party)
        refills = refills.filter(party=party)

    total_pending = 0
    for s in sales:
        total_paid = sum(p.amount for p in s.payment_set.all())
        total_pending += s.total_amount - total_paid
    for r in refills:
        total_paid = sum(p.amount for p in r.payment_set.all())
        total_pending += r.total_amount - total_paid
    return total_pending
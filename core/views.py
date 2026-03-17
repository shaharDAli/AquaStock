import csv
from django.shortcuts import render
from django.utils.timezone import now
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .dashboard import dashboard_summary
from .reports import production_report, sales_report, refill_report, pending_report
from products.models import LitreMaster
from parties.models import Party
from production.models import Production
from sales.models import Sale
from refill.models import Refill

# -------------------------
# Home Dashboard View
# -------------------------
def home_dashboard(request):
    today = now().date()

    today_production = Production.objects.filter(created_at__date=today).count()
    today_sales = Sale.objects.filter(created_at__date=today).count()
    today_refill = Refill.objects.filter(created_at__date=today).count()

    pending_parties = Party.objects.filter(is_active=True).count()

    context = {
        "today_production": today_production,
        "today_sales": today_sales,
        "today_refill": today_refill,
        "pending_parties": pending_parties,
    }

    return render(request, "core/dashboard.html", context)


# =========================
# CSV Export Functions
# =========================
def export_production_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="production.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Litre', 'Quantity', 'Created At'])

    for p in Production.objects.all():
        writer.writerow([p.id, p.litre.name, p.quantity, p.created_at])

    return response


def export_sales_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Party / Customer', 'Litre', 'Quantity', 'Unit Price', 'Total Amount', 'Payment Status', 'Date'])

    for s in Sale.objects.all():
        party_name = s.party.name if s.party else s.customer_name
        writer.writerow([s.id, party_name, s.litre.name, s.quantity, s.unit_price, s.total_amount, s.get_payment_status_display(), s.created_at])

    return response


def export_refill_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="refill_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Party / Customer', 'Quantity', 'Unit Price', 'Total Amount', 'Payment Status', 'Date'])

    for r in Refill.objects.all():
        party_name = r.party.name if r.party else r.customer_name
        writer.writerow([r.id, party_name, r.quantity, r.unit_price, r.total_amount, r.get_payment_status_display(), r.created_at])

    return response


def export_pending_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pending_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Party', 'Total Sales', 'Total Refill', 'Total Paid', 'Outstanding Amount'])

    for p in Party.objects.filter(is_active=True):
        writer.writerow([p.name, p.total_sales_amount, p.total_refill_amount, p.total_paid_amount, p.outstanding_amount])

    return response


# =========================
# Report Views
# =========================
def production_report_view(request):

    litres = LitreMaster.objects.all()

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    litre_id = request.GET.get("litre")
    search = request.GET.get("search")

    litre = LitreMaster.objects.filter(id=litre_id).first() if litre_id else None

    qs = production_report(start_date=start_date, end_date=end_date, litre=litre)

    if search:
        qs = qs.filter(litre__name__icontains=search)

    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "core/production_report.html",
        {
            "productions": page_obj,
            "litres": litres
        }
    )

def sales_report_view(request):

    litres = LitreMaster.objects.all()
    parties = Party.objects.all()

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    litre_id = request.GET.get("litre")
    party_id = request.GET.get("party")
    search = request.GET.get("search")

    litre = LitreMaster.objects.filter(id=litre_id).first() if litre_id else None
    party = Party.objects.filter(id=party_id).first() if party_id else None

    qs = sales_report(
        start_date=start_date,
        end_date=end_date,
        litre=litre,
        party=party
    )

    if search:
        qs = qs.filter(
            Q(customer_name__icontains=search) |
            Q(party__name__icontains=search)
        )

    paginator = Paginator(qs, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "core/sales_report.html",
        {
            "sales": page_obj,
            "litres": litres,
            "parties": parties
        }
    )

def refill_report_view(request):

    parties = Party.objects.all()

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    party_id = request.GET.get("party")
    search = request.GET.get("search")

    party = Party.objects.filter(id=party_id).first() if party_id else None

    qs = refill_report(start_date=start_date, end_date=end_date, party=party)

    if search:
        qs = qs.filter(
            Q(customer_name__icontains=search) |
            Q(party__name__icontains=search)
        )

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "core/refill_report.html",
        {
            "refills": page_obj,
            "parties": parties
        },
    )

def pending_report_view(request):

    search = request.GET.get("search")

    parties = Party.objects.filter(is_active=True)

    if search:
        parties = parties.filter(name__icontains=search)

    paginator = Paginator(parties, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "core/pending_report.html",
        {
            "parties": page_obj
        },
    )


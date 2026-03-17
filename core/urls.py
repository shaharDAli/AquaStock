from django.urls import path
from . import views
from production.models import Production

urlpatterns = [
    path("", views.home_dashboard, name="home_dashboard"),
    path("reports/production/", views.production_report_view, name="production_report"),
    path("reports/sales/", views.sales_report_view, name="sales_report"),
    path("reports/refill/", views.refill_report_view, name="refill_report"),
    path("reports/pending/", views.pending_report_view, name="pending_report"),
    path('reports/production/csv/', views.export_production_csv, name='export_production_csv'),
    path('reports/sales/csv/', views.export_sales_csv, name='export_sales_csv'),
    path('reports/refill/csv/', views.export_refill_csv, name='export_refill_csv'),
    path('reports/pending/csv/', views.export_pending_csv, name='export_pending_csv'),

]
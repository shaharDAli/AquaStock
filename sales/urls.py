from django.urls import path
from . import views

urlpatterns = [

    path("", views.sales_list, name="sales_list"),

    path("add/", views.sales_add, name="sales_add"),

]
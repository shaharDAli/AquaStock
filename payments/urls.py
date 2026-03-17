from django.urls import path
from . import views

urlpatterns = [

    path("sale/<int:sale_id>/", views.payment_add, name="sale_payment_add"),

    path("refill/<int:refill_id>/", views.payment_add, name="refill_payment_add"),

    path("history/<int:sale_id>/", views.payment_history, name="payment_history"),

]
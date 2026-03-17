from django.urls import path
from .views import *

urlpatterns = [

    path("litres/", litre_list, name="litre_list"),

    path("litres/add/", litre_add, name="litre_add"),

    path("litres/edit/<int:pk>/", litre_edit, name="litre_edit"),

    path("litres/deactivate/<int:pk>/", litre_deactivate, name="litre_deactivate"),
]
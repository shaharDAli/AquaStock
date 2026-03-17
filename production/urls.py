from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.production_list,
        name="production_list"
    ),

    path(
        "add/",
        views.production_add,
        name="production_add"
    ),

    path(
    "edit/<int:pk>/",
    views.production_edit,
    name="production_edit"
    ),

]
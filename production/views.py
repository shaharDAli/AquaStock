from django.shortcuts import render, redirect, get_object_or_404
from .models import Production
from products.models import LitreMaster
from django.core.paginator import Paginator
from django.db.models import Q


def production_list(request):

    search = request.GET.get("search")

    productions = Production.objects.all().order_by("-created_at")

    if search:
        productions = productions.filter(
            Q(litre__name__icontains=search) |
            Q(notes__icontains=search)
        )

    paginator = Paginator(productions, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "production/production_list.html",
        {
            "productions": page_obj
        }
    )


def production_add(request):

    litres = LitreMaster.objects.filter(is_active=True)

    if request.method == "POST":

        litre_id = request.POST.get("litre")
        quantity = request.POST.get("quantity")

        litre = LitreMaster.objects.get(id=litre_id)

        Production.objects.create(
            litre=litre,
            quantity=quantity
        )

        return redirect("production_list")

    return render(
        request,
        "production/production_add.html",
        {"litres": litres}
    )

def production_edit(request, pk):

    production = get_object_or_404(Production, pk=pk)
    litres = LitreMaster.objects.filter(is_active=True)

    if request.method == "POST":

        litre_id = request.POST.get("litre")
        quantity = request.POST.get("quantity")
        notes = request.POST.get("notes")

        production.litre = LitreMaster.objects.get(id=litre_id)
        production.quantity = quantity
        production.notes = notes
        production.save()

        return redirect("production_list")

    return render(
        request,
        "production/production_edit.html",
        {
            "production": production,
            "litres": litres
        }
    )
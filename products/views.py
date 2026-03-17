from django.shortcuts import render, redirect, get_object_or_404
from .models import LitreMaster


# Litre List
def litre_list(request):
    litres = LitreMaster.objects.filter(is_active=True)
    return render(request, "products/litre_list.html", {"litres": litres})


# Add Litre
def litre_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")

        LitreMaster.objects.create(
            name=name,
            current_price=price
        )

        return redirect("litre_list")

    return render(request, "products/litre_add.html")


# Edit Litre
def litre_edit(request, pk):
    litre = get_object_or_404(LitreMaster, pk=pk)

    if request.method == "POST":
        litre.name = request.POST.get("name")
        litre.current_price = request.POST.get("price")
        litre.save()

        return redirect("litre_list")

    return render(request, "products/litre_edit.html", {"litre": litre})


# Deactivate Litre
def litre_deactivate(request, pk):
    litre = get_object_or_404(LitreMaster, pk=pk)
    litre.is_active = False
    litre.save()

    return redirect("litre_list")


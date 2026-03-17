from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from products.models import LitreMaster
from parties.models import Party
from .models import Sale


def sales_add(request):

    litres = LitreMaster.objects.filter(is_active=True)
    parties = Party.objects.filter(is_active=True)

    error = None

    if request.method == "POST":

        litre_id = request.POST.get("litre")
        quantity = request.POST.get("quantity")
        customer_type = request.POST.get("customer_type")
        party_id = request.POST.get("party")

        if not quantity:
            error = "Quantity is required"
        else:

            quantity = int(quantity)

            litre = LitreMaster.objects.get(id=litre_id)

            # Stock validation
            if quantity > litre.current_stock:
                error = "Not enough stock available"

            else:

                party = None

                if customer_type == "PROVIDER":
                    if not party_id:
                        error = "Provider sale must have a party"
                    else:
                        party = Party.objects.get(id=party_id)

                if not error:

                    sale = Sale(
                        litre=litre,
                        quantity=quantity,
                        customer_type=customer_type,
                        party=party,
                        unit_price=litre.current_price
                    )

                    sale.full_clean()
                    sale.save()

                    return redirect("sales_list")

    return render(
        request,
        "sales/sales_add.html",
        {
            "litres": litres,
            "parties": parties,
            "error": error
        }
    )


def sales_list(request):

    sales = Sale.objects.all().order_by("-created_at")

    return render(
        request,
        "sales/sales_list.html",
        {
            "sales": sales
        }
    )
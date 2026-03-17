from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum


class LitreMaster(models.Model):
    name = models.CharField(max_length=50)  # 20L, 1L, 500ml
    current_price = models.DecimalField(max_digits=10, decimal_places=2)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ❌ No Delete Policy
    def delete(self, *args, **kwargs):
        raise ValidationError("Delete not allowed. Deactivate instead.")

    @property
    def current_stock(self):
        from production.models import Production
        from sales.models import Sale
        total_production = Production.objects.filter(litre=self).aggregate(total=Sum('quantity'))['total'] or 0
        total_sales = Sale.objects.filter(litre=self).aggregate(total=Sum('quantity'))['total'] or 0
        return total_production - total_sales

    def __str__(self):
        return self.name

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum


class Party(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ❌ No Delete Policy
    def delete(self, *args, **kwargs):
        raise ValidationError("Delete not allowed. Deactivate instead.")

    # 💰 Total Sales Amount
    @property
    def total_sales_amount(self):
        from sales.models import Sale
        return sum(s.total_amount for s in Sale.objects.filter(party=self))

    # 💰 Total Refill Amount
    @property
    def total_refill_amount(self):
        from refill.models import Refill
        return sum(r.total_amount for r in Refill.objects.filter(party=self))

    # 💰 Total Paid Amount
    @property
    def total_paid_amount(self):
        from payments.models import Payment

        sale_payments = Payment.objects.filter(
            sale__party=self
        ).aggregate(total=Sum("amount"))["total"] or 0

        refill_payments = Payment.objects.filter(
            refill__party=self
        ).aggregate(total=Sum("amount"))["total"] or 0

        return sale_payments + refill_payments

    # 💰 Final Outstanding
    @property
    def outstanding_amount(self):
        return (
            self.total_sales_amount
            + self.total_refill_amount
            - self.total_paid_amount
        )

    def __str__(self):
        return self.name
from django.db import models
from django.core.exceptions import ValidationError
from sales.models import Sale
from refill.models import Refill


class Payment(models.Model):

    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, null=True, blank=True)
    refill = models.ForeignKey(Refill, on_delete=models.CASCADE, null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        # Must link to either sale or refill
        if not self.sale and not self.refill:
            raise ValidationError("Payment must be linked to Sale or Refill.")

        # Cannot link to both
        if self.sale and self.refill:
            raise ValidationError("Payment cannot link to both.")

        # Overpayment protection for Sale
        if self.sale:
            total_paid = sum(p.amount for p in self.sale.payment_set.all())
            if total_paid + self.amount > self.sale.total_amount:
                raise ValidationError("Overpayment not allowed.")

        # Overpayment protection for Refill
        if self.refill:
            total_paid = sum(p.amount for p in self.refill.payment_set.all())
            if total_paid + self.amount > self.refill.total_amount:
                raise ValidationError("Overpayment not allowed.")

    def __str__(self):
        return f"Payment - {self.amount}"
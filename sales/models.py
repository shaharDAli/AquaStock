from django.db import models
from django.core.exceptions import ValidationError
from products.models import LitreMaster
from parties.models import Party


class Sale(models.Model):

    WALK_IN = "WALK_IN"
    PROVIDER = "PROVIDER"

    CUSTOMER_TYPE_CHOICES = [
        (WALK_IN, "Walk-in"),
        (PROVIDER, "Provider"),
    ]

    litre = models.ForeignKey(LitreMaster, on_delete=models.PROTECT)
    party = models.ForeignKey(Party, on_delete=models.PROTECT, null=True, blank=True)

    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES)

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    # ❌ No delete policy
    def delete(self, *args, **kwargs):
        raise ValidationError("Delete not allowed. Only quantity editable.")

    def clean(self):

        # Walk-in → party must be empty
        if self.customer_type == self.WALK_IN:
            self.party = None

        # Provider → party required
        if self.customer_type == self.PROVIDER and not self.party:
            raise ValidationError("Provider sale must have a party.")

    @property
    def total_amount(self):
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):

        if not self.unit_price:
            self.unit_price = self.litre.current_price

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.litre.name} - {self.quantity}"

    @property
    def payment_status(self):

        total_paid = sum(p.amount for p in self.payment_set.all())

        if total_paid == 0:
            return "Pending"
        elif total_paid < self.total_amount:
            return "Partial"
        else:
            return "Paid"
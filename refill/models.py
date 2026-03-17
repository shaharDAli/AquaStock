from django.db import models
from django.core.exceptions import ValidationError
from products.models import LitreMaster
from parties.models import Party


class Refill(models.Model):

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

    # 🔐 Snapshot price
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        # ✅ Allow only 20L refill
        if self.litre.name != "20L":
            raise ValidationError("Refill allowed only for 20L.")

        if self.customer_type == self.WALK_IN and self.party:
            raise ValidationError("Walk-in refill should not have a party.")

        if self.customer_type == self.PROVIDER and not self.party:
            raise ValidationError("Provider refill must have a party.")

    @property
    def total_amount(self):
        return self.quantity * self.unit_price

    def save(self, *args, **kwargs):
        # Snapshot price
        if not self.unit_price:
            self.unit_price = self.litre.current_price
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Delete not allowed. Only quantity editable.")

    def __str__(self):
        return f"Refill - {self.quantity}"
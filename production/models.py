from django.db import models
from django.core.exceptions import ValidationError
from products.models import LitreMaster


class Production(models.Model):
    litre = models.ForeignKey(LitreMaster, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    # ❌ No Delete Policy
    def delete(self, *args, **kwargs):
        raise ValidationError("Delete not allowed. Only quantity editable.")

    def __str__(self):
        return f"{self.litre.name} - {self.quantity}"
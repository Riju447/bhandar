from django.db import models

from suppliers.models import Supplier


class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchases')
    invoice_number = models.CharField(max_length=50, unique=True)
    purchase_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.invoice_number

from django.db import models


class BusinessSettings(models.Model):
    company_name = models.CharField(max_length=200, default='Inventory System')
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    invoice_prefix = models.CharField(max_length=20, default='INV')

    def __str__(self):
        return self.company_name

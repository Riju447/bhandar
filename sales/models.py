from django.db import models


class Sale(models.Model):
    customer_name = models.CharField(max_length=150, blank=True)
    sale_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, default='Cash')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'Sale {self.id}'

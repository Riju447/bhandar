from django.test import TestCase

from brands.models import Brand
from categories.models import Category
from suppliers.models import Supplier
from .models import Product


class ProductModelTests(TestCase):
    def test_product_stock_can_be_updated(self):
        category = Category.objects.create(name='Widgets')
        brand = Brand.objects.create(name='Acme')
        supplier = Supplier.objects.create(
            name='Supplier One',
            company_name='Acme Supply',
            email='supplier@example.com',
            phone='1234567890',
        )
        product = Product.objects.create(
            name='Widget',
            sku='WGT-001',
            barcode='123456789012',
            category=category,
            brand=brand,
            supplier=supplier,
            purchase_price=10.00,
            selling_price=15.00,
            quantity=5,
            minimum_stock=2,
        )

        product.quantity += 3
        product.save()

        self.assertEqual(Product.objects.get(pk=product.pk).quantity, 8)

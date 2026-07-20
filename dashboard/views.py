from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Sum
from django.views.generic import TemplateView

from brands.models import Brand
from categories.models import Category
from products.models import Product
from purchases.models import Purchase
from sales.models import Sale
from suppliers.models import Supplier


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_products'] = Product.objects.count()
        context['total_categories'] = Category.objects.count()
        context['total_suppliers'] = Supplier.objects.count()
        context['total_brands'] = Brand.objects.count()
        context['total_purchases'] = Purchase.objects.count()
        context['total_sales'] = Sale.objects.count()
        context['total_revenue'] = Sale.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        context['monthly_profit'] = 0
        context['low_stock_products'] = Product.objects.filter(quantity__lte=F('minimum_stock'))
        context['latest_products'] = Product.objects.order_by('-created_at')[:6]

        monthly_sales = defaultdict(int)
        monthly_revenue = defaultdict(float)
        for sale in Sale.objects.order_by('sale_date'):
            month_key = sale.sale_date.strftime('%b')
            monthly_sales[month_key] += 1
            monthly_revenue[month_key] += float(sale.total_amount)

        monthly_labels = list(monthly_sales.keys())[-6:]
        monthly_sales_data = [monthly_sales[label] for label in monthly_labels]
        monthly_revenue_data = [round(monthly_revenue[label], 2) for label in monthly_labels]

        max_value = max([*monthly_sales_data, *monthly_revenue_data], default=1)
        chart_points = []
        for label, sales_count, revenue_total in zip(monthly_labels, monthly_sales_data, monthly_revenue_data):
            scale = 24 if max_value <= 1 else max(30, int((max(revenue_total, sales_count) / max_value) * 140))
            chart_points.append({
                'label': label,
                'sales': sales_count,
                'revenue': revenue_total,
                'sales_height': scale if sales_count else 24,
                'revenue_height': scale if revenue_total else 24,
            })

        context['monthly_data'] = chart_points
        return context

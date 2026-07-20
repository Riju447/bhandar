from django.urls import path

from .views import MonthlySalesRevenueCreateView, SaleCreateView, SaleListView

app_name = 'sales'

urlpatterns = [
    path('', SaleListView.as_view(), name='sale_list'),
    path('create/', SaleCreateView.as_view(), name='sale_create'),
    path('monthly-entry/', MonthlySalesRevenueCreateView.as_view(), name='monthly_entry'),
]

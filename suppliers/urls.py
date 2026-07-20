from django.urls import path

from .views import SupplierCreateView, SupplierDeleteView, SupplierListView, SupplierUpdateView

app_name = 'suppliers'

urlpatterns = [
    path('', SupplierListView.as_view(), name='supplier_list'),
    path('create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('<int:pk>/edit/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier_delete'),
]

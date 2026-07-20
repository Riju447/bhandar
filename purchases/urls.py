from django.urls import path

from .views import PurchaseCreateView, PurchaseListView

app_name = 'purchases'

urlpatterns = [
    path('', PurchaseListView.as_view(), name='purchase_list'),
    path('create/', PurchaseCreateView.as_view(), name='purchase_create'),
]

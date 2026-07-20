from django.urls import path

from .views import BrandCreateView, BrandDeleteView, BrandListView, BrandUpdateView

app_name = 'brands'

urlpatterns = [
    path('', BrandListView.as_view(), name='brand_list'),
    path('create/', BrandCreateView.as_view(), name='brand_create'),
    path('<int:pk>/edit/', BrandUpdateView.as_view(), name='brand_update'),
    path('<int:pk>/delete/', BrandDeleteView.as_view(), name='brand_delete'),
]

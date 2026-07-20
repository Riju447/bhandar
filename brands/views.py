from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import BrandForm
from .models import Brand


class BrandListView(LoginRequiredMixin, ListView):
    model = Brand
    template_name = 'brands/brand_list.html'
    context_object_name = 'brands'


class BrandCreateView(LoginRequiredMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'brands/brand_form.html'
    success_url = reverse_lazy('brands:brand_list')


class BrandUpdateView(LoginRequiredMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'brands/brand_form.html'
    success_url = reverse_lazy('brands:brand_list')


class BrandDeleteView(LoginRequiredMixin, DeleteView):
    model = Brand
    template_name = 'brands/brand_confirm_delete.html'
    success_url = reverse_lazy('brands:brand_list')

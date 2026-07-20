from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView

from .models import Sale


class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    ordering = ['-sale_date', '-id']


class SaleCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    template_name = 'sales/sale_form.html'
    fields = ['customer_name', 'total_amount', 'discount', 'tax', 'payment_method', 'notes']
    success_url = '/sales/'

    def form_valid(self, form):
        messages.success(self.request, 'Sale recorded successfully.')
        return super().form_valid(form)


class MonthlySalesRevenueCreateView(LoginRequiredMixin, CreateView):
    model = Sale
    template_name = 'sales/monthly_summary_form.html'
    fields = ['customer_name', 'sale_date', 'total_amount', 'discount', 'tax', 'payment_method', 'notes']
    success_url = '/sales/monthly-entry/'

    def form_valid(self, form):
        messages.success(self.request, 'Monthly sales and revenue entry saved successfully.')
        return super().form_valid(form)

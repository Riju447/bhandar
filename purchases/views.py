from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView

from suppliers.models import Supplier
from .models import Purchase


class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'purchases/purchase_list.html'
    context_object_name = 'purchases'
    ordering = ['-purchase_date', '-id']


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    template_name = 'purchases/purchase_form.html'
    fields = ['supplier', 'invoice_number', 'total_amount', 'notes']
    success_url = '/purchases/'

    def form_valid(self, form):
        messages.success(self.request, 'Purchase recorded successfully.')
        return super().form_valid(form)

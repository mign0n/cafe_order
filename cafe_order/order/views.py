from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from order import forms
from order import models


class OrderCreateView(CreateView):
    model = models.Order
    form_class = forms.OrderForm
    success_url = reverse_lazy('order:order')
    template_name = 'order/order_create.html'


class MealsCreateView(CreateView):
    model = models.Meal
    form_class = forms.MealForm
    success_url = reverse_lazy('order:meal')
    template_name = 'order/meal_create.html'


class OrderListView(ListView):
    model = models.Order
    template_name = 'order/order_list.html'
    form_class = forms.SearchOrderForm

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            self.template_name,
            {'form': self.form_class(), 'orders': self.model.objects.all()},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            table_number = data.get('table_number')
            status = data.get('status')

            filters = {}
            if table_number:
                filters['table_number'] = table_number
            if status:
                filters['status'] = status

            orders = self.model.objects.filter(**filters)
        else:
            orders = self.model.objects.none()
        
        return render(
            request,
            self.template_name,
            {'form': form, 'orders': orders},
        )


class OrderDeleteView(DeleteView):
    model = models.Order
    success_url = reverse_lazy('order:order_list')

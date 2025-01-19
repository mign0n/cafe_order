from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView

from order.models import Meal, Order


class OrderCreateView(CreateView):
    model = Order
    fields = ('table_number', 'items')
    success_url = reverse_lazy('order:order')
    template_name = 'order/order_create.html'


class MealsCreateView(CreateView):
    model = Meal
    fields = ('name', 'price')
    success_url = reverse_lazy('order:meal')
    template_name = 'order/meal_create.html'


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('order:order-list')

from django.urls import path

from order.views import MealsCreateView, OrderCreateView, OrderListView


app_name = '%(app_label)s'

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('order/', OrderCreateView.as_view(), name='order'),
    path('meal/', MealsCreateView.as_view(), name='meal'),
]

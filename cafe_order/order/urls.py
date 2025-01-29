from django.urls import path

from order.views import (
    CurrentDayRevenueView,
    MealsCreateView,
    OrderCreateView,
    OrderDeleteView,
    OrderListView,
    OrderUpdateView,
)

app_name = '%(app_label)s'

urlpatterns = [
    path('', OrderListView.as_view(), name='order_list'),
    path('meal/', MealsCreateView.as_view(), name='meal'),
    path('order/', OrderCreateView.as_view(), name='order'),
    path(
        'order/<int:pk>/delete',
        OrderDeleteView.as_view(),
        name='order_delete',
    ),
    path(
        'order/<int:pk>/change',
        OrderUpdateView.as_view(),
        name='order_update',
    ),
    path('revenue/', CurrentDayRevenueView.as_view(), name='revenue'),
]

from django.urls import path

from order.views import (
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
        'order/<int:pk>/change-status',
        OrderUpdateView.as_view(),
        name='order_update',
    ),
]

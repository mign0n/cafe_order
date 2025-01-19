from django.urls import path

from order.views import (
    MealsCreateView,
    OrderCreateView,
    OrderDeleteView,
    OrderListView,
)


app_name = '%(app_label)s'

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('meal/', MealsCreateView.as_view(), name='meal'),
    path('order/', OrderCreateView.as_view(), name='order'),
    path(
        'order/<int:pk>/delete',
        OrderDeleteView.as_view(),
        name='order-delete',
    ),
]

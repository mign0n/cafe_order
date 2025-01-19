from django.urls import path

from order.views import MealsCreateView, OrderCreateView


app_name = '%(app_label)s'

urlpatterns = [
    path('order/', OrderCreateView.as_view(), name='order'),
    path('meal/', MealsCreateView.as_view(), name='meal'),
]

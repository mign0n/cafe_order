from django.urls import include
from rest_framework.routers import DefaultRouter, path

from api.views import MealViewSet, OrderViewSet

router = DefaultRouter()
router.register('meals', MealViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

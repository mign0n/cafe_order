from core.constants import (
    DELETE_PROHIBITED_MESSAGE,
    UPDATE_PROHIBITED_MESSAGE,
    OrderStatus,
)
from django.db.models import Model
from order.models import Meal, Order
from rest_framework import filters, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import MealSerializer, OrderSerializer


class MealViewSet(viewsets.ModelViewSet):
    """Представление для работы с объектами блюд.

    Атрибуты:
        queryset: Все объекты блюд.
        serializer_class: Сериализатор для объектов блюд.
    """

    queryset = Meal.objects.all()
    serializer_class = MealSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Представление для работы с объектами заказов.

    Атрибуты:
        queryset: Все объекты заказов.
        serializer_class: Сериализатор для объектов заказов.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('table_number', 'status')

    @action(methods=('GET',), detail=False)
    def revenue(self, request: Request) -> Response:
        """Получение дохода за текущий день.

        Возвращает сумму всех оплаченных заказов за текущую дату.

        Аргументы:
            request: Запрос от клиента.

        Возвращает:
            Ответ с суммой дохода за текущую дату.
        """
        return Response(Order.objects.get_revenue_for_day())

    def perform_update(self, serializer: serializers.Serializer) -> None:
        """Проверяет статус заказа перед обновлением заказа.

        Raises:
            ValidationError: Если статус заказа `OrderStatus.PAID_FOR`
        """
        if serializer.data.get('status') == OrderStatus.PAID_FOR:
            raise serializers.ValidationError(UPDATE_PROHIBITED_MESSAGE)
        super().perform_update(serializer)

    def perform_destroy(self, instance: Model) -> None:
        """Проверяет статус заказа перед удалением заказа.

        Raises:
            ValidationError: Если статус заказа `OrderStatus.PAID_FOR`
        """
        if instance.status == OrderStatus.PAID_FOR:
            raise serializers.ValidationError(DELETE_PROHIBITED_MESSAGE)
        super().perform_destroy(instance)

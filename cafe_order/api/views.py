from django.db.models import Sum
from django.utils.timezone import datetime
from order.constants import OrderStatus
from order.models import Meal, Order
from rest_framework import viewsets
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

    @action(methods=('GET',), detail=False)
    def revenue(self, request: Request) -> Response:
        """Получение дохода за текущий день.

        Возвращает сумму всех оплаченных заказов за текущую дату.

        Аргументы:
            request: Запрос от клиента.

        Возвращает:
            Ответ с суммой дохода за текущую дату.
        """
        return Response(
            self.queryset.filter(
                status=OrderStatus.PAID_FOR,
                created_at__date=datetime.now().date(),
            ).annotate(
                total_price=Sum('items__price'),
            ).aggregate(
                revenue_per_shift=Sum('total_price', default=0),
            ),
        )

from order.models import Meal, Order
from rest_framework import filters, viewsets
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

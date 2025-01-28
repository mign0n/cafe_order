from order.models import Meal, Order
from rest_framework import serializers


class MealSerializer(serializers.ModelSerializer):
    """Сериализатор модели блюд."""

    class Meta:
        """Метаданные сериализатора.

        Определяет модель и поля для сериализации.

        Attributes:
            model: Модель, к которой привязан сериализатор.
            fields: Поля модели для сериализации.
        """

        model = Meal
        fields = (
            'id',
            'name',
            'price',
        )


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор модели заказов.

    Attributes:
        items: Объект с данными о блюдах.
    """

    items = MealSerializer(many=True)

    class Meta:
        """Метаданные сериализатора.

        Определяет модель и поля для сериализации.

        Attributes:
            model: Модель, к которой привязан сериализатор.
            fields: Поля модели для сериализации.
        """

        model = Order
        fields = (
            'id',
            'table_number',
            'items',
            'price',
            'status',
            'created_at',
        )

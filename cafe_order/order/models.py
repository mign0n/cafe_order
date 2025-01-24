from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.utils import cached_property

from order.constants import OrderStatus


class Meal(models.Model):
    """Модель блюда.

    Attributes:
        name: Название блюда.
        price: Цена блюда.
    """

    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    def __str__(self) -> str:
        """Возвращает строковое представление объекта блюда."""
        return f'{type(self).__name__} #{self.pk}: {self.name} - {self.price}'


class Order(models.Model):
    """Модель заказа.

    Attributes:
        items: Блюда, входящие в заказ.
        table_number: Номер стола, за которым был сделан заказ.
        status: Статус заказа.
        created_at: Время создания заказа.
    """

    items = models.ManyToManyField(
        Meal,
        related_name='order_meals',
    )
    table_number = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
    )
    status = models.CharField(
        choices=OrderStatus,
        default=OrderStatus.WAITING,
        max_length=10,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @cached_property
    def total_price(self) -> Decimal:
        """Возвращает общую стоимость всех блюд в заказе."""
        return self.items.values('order_meals').aggregate(
            total_price=models.Sum('price'),
        ).get('total_price')

    def __str__(self) -> str:
        """Возвращает строковое представление объекта заказа."""
        return (
            f'{type(self).__name__} #{self.pk}: '
            f'{self.table_number} - {self.status}'
        )

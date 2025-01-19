from django.core.validators import MinValueValidator
from django.db import models

from order.constants import OrderStatus


class Meal(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f'{type(self).__name__} #{self.pk}: {self.name} - {self.price}'


class Order(models.Model):
    items = models.ManyToManyField(Meal, related_name='order_meals')
    table_number = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
    )
    status = models.CharField(
        choices=OrderStatus,
        default=OrderStatus.WAITING,
        max_length=10,
    )

    def __str__(self) -> str:
        return (
            f'{type(self).__name__} #{self.pk}: '
            f'{self.table_number} - {self.status}'
        )

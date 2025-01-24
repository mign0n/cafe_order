from django.db import models


class OrderStatus(models.TextChoices):
    """Варианты выбора статуса заказа.

    Attributes:
        EMPTY:
        WAITING:
        READY:
        PAID_FOR:
    """

    EMPTY = '', '----------'
    WAITING = 'WAITING', 'Waiting'
    READY = 'READY', 'Ready'
    PAID_FOR = 'PAID_FOR', 'Paid for'

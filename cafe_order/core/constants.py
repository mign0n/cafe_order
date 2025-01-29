from django.db import models

DELETE_PROHIBITED_MESSAGE = 'Deleting a paid order is prohibited.'
UPDATE_PROHIBITED_MESSAGE = 'Changing a paid order is prohibited.'


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

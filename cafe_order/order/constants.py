from django.db import models


class OrderStatus(models.TextChoices):
    EMPTY = '', '----------'
    WAITING = 'WAITING', 'Waiting'
    READY = 'READY', 'Ready'
    PAID_FOR = 'PAID_FOR', 'Paid for'

from django.db import models


class OrderStatus(models.TextChoices):
    WAITING = 'WAITING', 'В ожидании'
    READY = 'READY', 'Готов'
    PAID_FOR = 'PAID_FOR', 'Оплаченный'

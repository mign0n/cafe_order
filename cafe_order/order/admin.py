from django.contrib import admin

from order import models


@admin.register(models.Meal)
class MealAdmin(admin.ModelAdmin):
    """Блюдо в панели администратора.

    Определяет отображение модели Meal в админ-панели.

    Attributes:
        list_display: Список полей для отображения.
    """

    list_display = (
        'id',
        'name',
        'price',
    )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """Заказ в панели администратора.

    Определяет отображение модели Order в админ-панели.

    Attributes:
        list_display: Список полей для отображения.
    """

    list_display = (
        'id',
        'table_number',
        'status',
    )

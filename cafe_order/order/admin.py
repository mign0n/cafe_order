from django.contrib import admin

from order import models


@admin.register(models.Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
    )


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'table_number',
        'status',
    )

from django import forms

from order.constants import OrderStatus
from order.models import Meal, Order


class OrderForm(forms.ModelForm):
    """Форма для создания заказа."""

    class Meta:
        """Метаданные формы.

        Определяет модель, поля и виджеты для формы.

        Attributes:
            model: Модель, к которой привязана форма.
            fields: Поля модели, включаемые в форму.
            widgets: Виджеты для полей формы.
        """

        model = Order
        fields = ('table_number', 'items')

        widgets = {
            'table_number': forms.NumberInput(
                attrs={'class': 'input-select'},
            ),
            'items': forms.SelectMultiple(
                attrs={
                    'class': 'input-select',
                    'size': 20,
                },
            ),
        }


class OrderUpdateForm(OrderForm):
    """Форма для редактирования заказа."""

    class Meta(OrderForm.Meta):
        """Метаданные формы.

        Определяет поля для формы.

        Attributes:
            fields: Поля модели, включаемые в форму.
        """

        fields = (
            'status',
            *OrderForm.Meta.fields,
        )


class MealForm(forms.ModelForm):
    """Форма для создания блюда."""

    class Meta:
        """Метаданные формы.

        Определяет модель, поля и виджеты для формы.

        Attributes:
            model: Модель, к которой привязана форма.
            fields: Поля модели, включаемые в форму.
            widgets: Виджеты для полей формы.
        """

        model = Meal
        fields = ('name', 'price')

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'input-select'},
            ),
            'price': forms.NumberInput(attrs={'class': 'input-select'}),
        }


class SearchOrderForm(forms.Form):
    """Форма поиска заказов.

    Attributes:
        table_number: Поле ввода номера стола.
        status: Поле выбора статуса заказа.
    """

    table_number = forms.IntegerField(required=False)
    status = forms.ChoiceField(choices=OrderStatus, required=False)

    class Meta:
        """Метаданные формы.

        Определяет виджеты для полей формы.

        Attributes:
            widgets: Виджеты для полей формы.
        """

        widgets = {
            'table_number': forms.NumberInput(
                attrs={'class': 'input-select'},
            ),
            'status': forms.Select(attrs={'class': 'input-select'}),
        }

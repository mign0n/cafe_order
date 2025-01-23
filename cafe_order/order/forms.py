from django import forms

from order.models import Meal, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('table_number', 'items')
        
        widgets = {
            'table_number': forms.NumberInput(attrs={'class': 'input-select'},),
            'items': forms.SelectMultiple(
                attrs={
                    'class': 'input-select',
                    'size': 20,
                },
            ),
        }


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ('name', 'price')
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-select'},),
            'price': forms.NumberInput(attrs={'class': 'input-select'}),
        }
import pytest
from core.constants import OrderStatus
from django.db.models import Model
from order.forms import MealForm, OrderForm, OrderUpdateForm, SearchOrderForm

pytestmark = pytest.mark.django_db


class TestMealForm:
    def test_valid_data(self) -> None:
        assert MealForm(data={'name': 'Пицца', 'price': 500}).is_valid()

    def test_invalid_data(self) -> None:
        assert not MealForm(data={'name': '', 'price': -500}).is_valid()


class TestOrderForm:
    def test_valid_data(self, order: Model) -> None:
        assert OrderForm(
            data={
                'table_number': order.table_number,
                'items': [meal.pk for meal in order.items.all()],
            },
            instance=order,
        ).is_valid()

    def test_invalid_data(self) -> None:
        form = OrderForm(data={'table_number': 9990})
        assert not form.is_valid()
        assert len(form.errors) == 2
        assert 'table_number' in form.errors
        assert 'items' in form.errors


class TestOrderUpdateForm:
    def test_valid_data(self, order: Model) -> None:
        assert OrderUpdateForm(
            data={
                'items': [1, 2],
                'table_number': order.table_number,
                'status': OrderStatus.READY,
            },
            instance=order,
        ).is_valid()

    def test_invalid_data(self) -> None:
        form = OrderForm(data={'table_number': 0})
        assert not form.is_valid()
        assert len(form.errors) == 2
        assert 'table_number' in form.errors
        assert 'items' in form.errors


class TestSearchOrderForm:
    def test_valid_data(self) -> None:
        assert SearchOrderForm(
            data={
                'table_number': 1,
                'status': OrderStatus.READY,
            }
        ).is_valid()

    def test_invalid_data(self) -> None:
        form = OrderForm(data={'table_number': -1})
        assert not form.is_valid()
        assert len(form.errors) == 2
        assert 'table_number' in form.errors
        assert 'items' in form.errors

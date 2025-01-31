from collections.abc import Callable
from http import HTTPStatus

import pytest
from core.constants import OrderStatus
from django.contrib.messages.storage.fallback import FallbackStorage
from django.db.models import Model
from django.test import RequestFactory
from django.urls import reverse
from order.forms import MealForm, OrderForm, OrderUpdateForm, SearchOrderForm
from order.models import Meal, Order
from order.views import (
    CurrentDayRevenueView,
    MealsCreateView,
    OrderCreateView,
    OrderDeleteView,
    OrderListView,
    OrderUpdateView,
)

pytestmark = pytest.mark.django_db


class TestMealsCreateView:
    @property
    def _view(self) -> Callable:
        return MealsCreateView.as_view()

    def test_get(self, rf: RequestFactory) -> None:
        response = self._view(rf.get(reverse('order:meal')))
        assert response.status_code == HTTPStatus.OK
        assert 'form' in response.context_data

    def test_post_valid_data(self, rf: RequestFactory) -> None:
        data = {
            'name': 'Пицца',
            'price': 500,
        }
        path = reverse('order:meal')
        response = self._view(rf.post(path, data))
        assert Meal.objects.filter(**data).exists()
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == path

    def test_post_invalid_data(self, rf: RequestFactory) -> None:
        data = {
            'name': '',
            'price': -500,
        }
        response = self._view(rf.post(reverse('order:meal'), data))
        assert not Meal.objects.filter(**data).exists()
        assert response.status_code == HTTPStatus.OK
        assert 'form' in response.context_data
        assert isinstance(response.context_data['form'], MealForm)
        assert len(response.context_data['form'].errors) == len(data)


class TestOrderCreateView:
    @property
    def _view(self) -> Callable:
        return OrderCreateView.as_view()

    def test_get(self, rf: RequestFactory) -> None:
        response = self._view(rf.get(reverse('order:order')))
        assert response.status_code == HTTPStatus.OK
        assert 'form' in response.context_data

    def test_post_valid_data(
        self,
        rf: RequestFactory,
        meals: list[Model],
    ) -> None:
        data = {
            'items': meals[0].pk,
            'table_number': 1,
        }
        path = reverse('order:order')
        response = self._view(rf.post(path, data))

        assert Order.objects.filter(
            **data,
            status=OrderStatus.WAITING,
        ).exists()
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == path

    def test_post_invalid_data(
        self,
        rf: RequestFactory,
        meals: list[Model],
    ) -> None:
        data = {
            'items': meals[0].pk,
            'table_number': -1,
        }
        response = self._view(rf.post(reverse('order:order'), data))
        assert not Order.objects.filter(**data).exists()
        assert response.status_code == HTTPStatus.OK
        assert 'form' in response.context_data
        assert isinstance(response.context_data['form'], OrderForm)
        assert len(response.context_data['form'].errors) > 0


class TestOrderListView:
    @property
    def _view(self) -> Callable:
        return OrderListView.as_view()

    def test_get_order_list_view(
        self,
        rf: RequestFactory,
        orders: list[Model],
    ) -> None:
        url = reverse('order:order_list')
        response = self._view(rf.get(url))
        assert response.status_code == 200
        assert isinstance(response.context_data['form'], SearchOrderForm)
        assert list(response.context_data['object_list']) == orders

    def test_post_order_list_view_with_valid_form_data(
        self,
        rf: RequestFactory,
        order: Model,
    ) -> None:
        url = reverse('order:order_list')
        data = {
            'table_number': order.table_number,
            'status': OrderStatus.WAITING,
        }
        response = self._view(rf.post(url, data))
        assert response.status_code == 200
        assert order.items.last().name in response.content.decode()

    def test_filter_orders_by_table_number(
        self,
        rf: RequestFactory,
        orders: list[Model],
    ) -> None:
        data = {'table_number': orders[0].table_number}
        response = self._view(
            rf.post(
                reverse('order:order_list'),
                data,
            ),
        )
        content = response.content.decode()
        assert response.status_code == 200
        for order in orders:
            if order.table_number == data['table_number']:
                assert str(order.table_number) in content
                assert order.items.last().name in content
            else:
                assert str(order.table_number) not in content

    def test_filter_orders_by_status(
        self,
        rf: RequestFactory,
        orders: list[Model],
        meals: list[Model],
    ) -> None:
        order_1 = Order.objects.create(
            table_number=10,
            status=OrderStatus.READY,
        )
        order_1.items.set(meals)
        orders.append(order_1)
        data = {'status': order_1.status}

        url = reverse('order:order_list')
        response = self._view(rf.post(url, data))

        content = response.content.decode()
        assert response.status_code == 200
        for order in orders:
            if order.status == data['status']:
                assert str(order.table_number) in content
                assert order.items.last().name in content
            else:
                assert str(order.table_number) not in content


class TestOrderUpdateView:
    @property
    def _view(self) -> Callable:
        return OrderUpdateView.as_view()

    def test_get(
        self,
        rf: RequestFactory,
        order: list[Model],
    ) -> None:
        kwargs = {'pk': order.pk}
        response = self._view(
            rf.get(reverse('order:order_update', kwargs=kwargs)),
            **kwargs,
        )
        assert response.status_code == HTTPStatus.OK
        assert 'form' in response.context_data
        assert isinstance(response.context_data['form'], OrderUpdateForm)

    def test_post_valid_data(
        self, rf: RequestFactory, order: Model, meals: list[Model]
    ) -> None:
        kwargs = {'pk': order.pk}
        data = {
            'items': meals[0].pk,
            'table_number': 2,
            'status': OrderStatus.READY,
        }
        response = self._view(
            rf.post(reverse('order:order_update', kwargs=kwargs), data),
            **kwargs,
        )

        assert Order.objects.filter(**data).exists()
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse('order:order_list')

    def test_post_invalid_data(
        self,
        rf: RequestFactory,
        order: Model,
        meals: list[Model],
    ) -> None:
        kwargs = {'pk': order.pk}
        data = {
            'items': meals[1].pk,
            'table_number': 0,
            'status': OrderStatus.READY,
        }
        response = self._view(
            rf.post(reverse('order:order_update', kwargs=kwargs), data),
            **kwargs,
        )

        assert not Order.objects.filter(**data).exists()
        assert response.status_code == HTTPStatus.OK
        assert 'form' in response.context_data
        assert isinstance(response.context_data['form'], OrderForm)
        assert len(response.context_data['form'].errors) > 0


class TestOrderDeleteView:
    @property
    def _view(self) -> Callable:
        return OrderDeleteView.as_view()

    def test_get(self, rf: RequestFactory, order: Model) -> None:
        kwargs = {'pk': order.pk}
        response = self._view(
            rf.get(reverse('order:order_delete', kwargs=kwargs)),
            **kwargs,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.context_data['object'] == order

    def test_post_valid_status(
        self,
        rf: RequestFactory,
        orders: list[Model],
    ) -> None:
        kwargs = {'pk': orders[0].pk}
        count = len(orders)
        response = self._view(
            rf.post(reverse('order:order_delete', kwargs=kwargs)),
            **kwargs,
        )

        assert not Order.objects.filter(**kwargs).exists()
        assert Order.objects.count() == count - 1
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse('order:order_list')

    def test_post_invalid_status(
        self,
        rf: RequestFactory,
        orders: list[Order],
    ) -> None:
        order = orders[0]
        order.status = OrderStatus.PAID_FOR
        order.save()
        kwargs = {'pk': order.pk}

        request = rf.post(reverse('order:order_delete', kwargs=kwargs))
        request.session = 'session'
        request._messages = FallbackStorage(request)
        response = self._view(request, **kwargs)

        assert Order.objects.filter(**kwargs).exists()
        assert response.status_code == HTTPStatus.FOUND
        assert response.url == reverse('order:order_list')


class TestCurrentDayRevenueView:
    @property
    def _view(self) -> Callable:
        return CurrentDayRevenueView.as_view()

    def test_get(self, rf: RequestFactory, paid_orders: list[Order]) -> None:
        response = self._view(rf.get(reverse('order:revenue')))

        assert response.status_code == HTTPStatus.OK
        assert (
            str(sum(order.price for order in paid_orders))[:6]
            in response.content.decode()
        )

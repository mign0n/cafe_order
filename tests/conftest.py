from collections.abc import Callable

import pytest
from core.constants import OrderStatus
from django.test import Client, RequestFactory
from factory.django import DjangoModelFactory

from tests.factories import MealFactory, OrderFactory


@pytest.fixture()
def fill_meal_batch() -> Callable:
    def wrap(meal_quantity: int = 5) -> DjangoModelFactory:
        return MealFactory.create_batch(meal_quantity)

    return wrap


@pytest.fixture()
def fill_order_batch() -> Callable:
    def wrap(
        order_quantity: int = 5,
        is_paid: bool = False,
    ) -> DjangoModelFactory:
        status = OrderStatus.WAITING
        if is_paid:
            status = OrderStatus.PAID_FOR
        factory = OrderFactory.create_batch(order_quantity, status=status)
        return factory

    return wrap


@pytest.fixture
def rf() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def client() -> Client:
    return Client()

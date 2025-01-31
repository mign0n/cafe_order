import pytest
from core.constants import OrderStatus
from django.test import RequestFactory
from mixer.backend.django import Mixer
from mixer.backend.django import mixer as _mixer
from order.models import Meal, Order


@pytest.fixture
def mixer() -> Mixer:
    return _mixer


@pytest.fixture
def meals(mixer: Mixer) -> list[Meal]:
    return mixer.cycle(5).blend('order.meal')


@pytest.fixture
def order(mixer, meals) -> list[Order]:
    return mixer.blend('order.order', items=meals)


@pytest.fixture
def orders(mixer, meals) -> list[Order]:
    return mixer.cycle(5).blend('order.order', items=meals)


@pytest.fixture
def paid_orders(mixer, meals) -> list[Order]:
    return mixer.cycle(5).blend(
        'order.order',
        items=meals,
        status=OrderStatus.PAID_FOR,
    )


@pytest.fixture
def rf() -> RequestFactory:
    return RequestFactory()

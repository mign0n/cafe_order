from collections.abc import Callable
from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class TestOrderURL:
    def test_order_list_url(self, client: Client) -> None:
        response = client.get(reverse('order:order_list'))
        assert response.status_code == HTTPStatus.OK
        assert 'order/order_list.html' in [
            template.name for template in response.templates
        ]

    def test_meal_create_url(self, client: Client) -> None:
        response = client.get(reverse('order:meal'))
        assert response.status_code == HTTPStatus.OK
        assert 'order/meal_create.html' in [
            template.name for template in response.templates
        ]

    def test_order_create_url(self, client: Client) -> None:
        response = client.get(reverse('order:order'))
        assert response.status_code == HTTPStatus.OK
        assert 'order/order_create.html' in [
            template.name for template in response.templates
        ]

    def test_order_delete_url(
        self,
        client: Client,
        fill_order_batch: Callable,
    ) -> None:
        response = client.get(
            reverse(
                'order:order_delete',
                kwargs={'pk': fill_order_batch(1)[0].pk},
            ),
        )
        assert response.status_code == HTTPStatus.OK
        assert 'order/order_confirm_delete.html' in [
            template.name for template in response.templates
        ]

    def test_order_update_url(
        self,
        client: Client,
        fill_order_batch: Callable,
    ) -> None:
        response = client.get(
            reverse(
                'order:order_update',
                kwargs={'pk': fill_order_batch(1)[0].pk},
            )
        )
        assert response.status_code == HTTPStatus.OK
        assert 'order/order_update.html' in [
            template.name for template in response.templates
        ]

    def test_revenue_url(self, client: Client) -> None:
        response = client.get(reverse('order:revenue'))
        assert response.status_code == HTTPStatus.OK
        assert 'order/revenue.html' in [
            template.name for template in response.templates
        ]

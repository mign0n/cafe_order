import json
from collections.abc import Callable

import pytest
from core.constants import OrderStatus
from order.models import Order
from rest_framework import status
from rest_framework.test import APIClient

ENDPOINT = '/api/v1/orders/'

pytestmark = pytest.mark.django_db


class TestGetOrders:
    def test_get_list(
        self,
        api_client: APIClient,
        fill_order_batch: Callable,
    ) -> None:
        orders = fill_order_batch()
        response = api_client.get(ENDPOINT)
        response_data = response.data
        assert response.status_code == status.HTTP_200_OK
        assert len(orders) == len(response_data)

    def test_get_by_id(
        self,
        api_client: APIClient,
        fill_order_batch: Callable,
    ) -> None:
        orders = fill_order_batch()
        order_id = orders[2].pk
        response = api_client.get(f'{ENDPOINT}{order_id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_get_by_non_existent_id(
        self,
        api_client: APIClient,
    ) -> None:
        response = api_client.get(f'{ENDPOINT}101/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_revenue_with_paid(
        self,
        api_client: APIClient,
        fill_order_batch: Callable,
    ) -> None:
        orders = fill_order_batch(is_paid=True)
        response = api_client.get(f'{ENDPOINT}revenue/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('revenue_per_shift') == sum(
            order.price for order in orders
        )

    def test_get_revenue_without_paid(
        self,
        api_client: APIClient,
        fill_order_batch: Callable,
    ) -> None:
        fill_order_batch()
        response = api_client.get(f'{ENDPOINT}revenue/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('revenue_per_shift') == 0


class TestPostOrders:
    def test_post_valid_data(
        self,
        api_client: APIClient,
        fill_meal_batch: Callable,
    ) -> None:
        body = {
            'table_number': 1,
            'items': [meal.pk for meal in fill_meal_batch()],
        }
        response = api_client.post(
            ENDPOINT,
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_201_CREATED
        for key, value in body.items():
            assert value == response.data.get(key)

    def test_post_invalid_data(
        self,
        api_client: APIClient,
    ) -> None:
        body = {
            'table_number': -1,
            'items': [],
        }
        response = api_client.post(
            ENDPOINT,
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestPatchOrders:
    def test_patch_valid_data(
        self,
        api_client: APIClient,
        fill_order_batch: Callable,
    ) -> None:
        orders = fill_order_batch()
        order_id = orders[2].pk
        body = {
            'table_number': 1,
            'items': [2, 3],
            'status': OrderStatus.READY,
        }
        response = api_client.patch(
            f'{ENDPOINT}{order_id}/',
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_200_OK
        for key, value in body.items():
            assert value == response.data.get(key)

    def test_patch_invalid_data(
        self,
        api_client: APIClient,
        fill_order_batch: Callable,
    ) -> None:
        orders = fill_order_batch()
        order_id = orders[2].pk
        body = {
            'table_number': -1,
            'items': [0, 3],
            'status': 'UNKNOWN',
        }
        response = api_client.patch(
            f'{ENDPOINT}{order_id}/',
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestPutOrders:
    def test_put_valid_data(
        self,
        api_client: APIClient,
        fill_order_batch: Callable,
    ) -> None:
        orders = fill_order_batch()
        order_id = orders[2].pk
        body = {
            'table_number': 10,
            'items': [2, 5],
        }
        response = api_client.put(
            f'{ENDPOINT}{order_id}/',
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_200_OK
        for key, value in body.items():
            assert value == response.data.get(key)

    def test_put_invalid_data(
        self,
        api_client: APIClient,
        fill_order_batch: Callable,
    ) -> None:
        orders = fill_order_batch()
        order_id = orders[2].pk
        body = {
            'table_number': -1,
            'items': [0, 3],
            'status': 'UNKNOWN',
        }
        response = api_client.put(
            f'{ENDPOINT}{order_id}/',
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteOrders:
    def test_delete_existent(
        self,
        api_client: APIClient,
        fill_order_batch: Callable,
    ) -> None:
        orders = fill_order_batch()
        order_id = orders[-1].pk
        response = api_client.delete(f'{ENDPOINT}{order_id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Order.objects.filter(pk=order_id).exists()

    def test_delete_paid_for(
        self,
        api_client: APIClient,
        fill_order_batch: Callable,
    ) -> None:
        orders = fill_order_batch(is_paid=True)
        order_id = orders[1].pk
        response = api_client.delete(f'{ENDPOINT}{order_id}/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert Order.objects.filter(pk=order_id).exists()

    def test_delete_non_existent(
        self,
        api_client: APIClient,
    ) -> None:
        response = api_client.delete(f'{ENDPOINT}101/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

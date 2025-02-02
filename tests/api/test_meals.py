import json
from collections.abc import Callable

import pytest
from django.db.models import Model
from order.models import Meal
from rest_framework import status
from rest_framework.test import APIClient

ENDPOINT = '/api/v1/meals/'

pytestmark = pytest.mark.django_db


class TestGetMeals:
    @staticmethod
    def make_fields_subtest(
        instance: Model,
        data: dict[str, str | int],
    ) -> None:
        fields = instance._meta.fields
        assert len(fields) == len(data)
        for field in fields:
            assert field.attname in data
            assert str(getattr(instance, field.attname)) == str(
                data.get(field.attname)
            )

    def test_get_list(
        self,
        api_client: APIClient,
        fill_meal_batch: Callable,
    ) -> None:
        meals = fill_meal_batch()
        response = api_client.get(ENDPOINT)
        response_data = response.data
        assert response.status_code == status.HTTP_200_OK
        assert len(meals) == len(response_data)
        for meal, data in zip(meals, response_data, strict=False):
            self.make_fields_subtest(meal, data)

    def test_get_by_id(
        self,
        api_client: APIClient,
        fill_meal_batch: Callable,
    ) -> None:
        meals = fill_meal_batch()
        meal_id = meals[2].pk
        response = api_client.get(f'{ENDPOINT}{meal_id}/')
        assert response.status_code == status.HTTP_200_OK
        self.make_fields_subtest(meals[2], response.data)

    def test_get_by_non_existent_id(
        self,
        api_client: APIClient,
    ) -> None:
        response = api_client.get(f'{ENDPOINT}101/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestPostMeals:
    def test_post_valid_data(
        self,
        api_client: APIClient,
    ) -> None:
        body = {
            'name': 'Паста Песто',
            'price': '130.00',
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
            'name': '',
            'price': '',
        }
        response = api_client.post(
            ENDPOINT,
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestPatchMeals:
    def test_patch_valid_data(
        self,
        api_client: APIClient,
        fill_meal_batch: Callable,
    ) -> None:
        meals = fill_meal_batch()
        meal_id = meals[2].pk
        body = {
            'name': 'Паста Песто',
            'price': '130.00',
        }
        response = api_client.patch(
            f'{ENDPOINT}{meal_id}/',
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_200_OK
        for key, value in body.items():
            assert value == response.data.get(key)

    def test_patch_invalid_data(
        self,
        api_client: APIClient,
        fill_meal_batch: Callable,
    ) -> None:
        meals = fill_meal_batch()
        meal_id = meals[2].pk
        body = {
            'name': '',
            'price': '',
        }
        response = api_client.patch(
            f'{ENDPOINT}{meal_id}/',
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestPutMeals:
    def test_put_valid_data(
        self,
        api_client: APIClient,
        fill_meal_batch: Callable,
    ) -> None:
        meals = fill_meal_batch()
        meal_id = meals[2].pk
        body = {
            'name': 'Паста Песто',
            'price': '130.00',
        }
        response = api_client.put(
            f'{ENDPOINT}{meal_id}/',
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_200_OK
        for key, value in body.items():
            assert value == response.data.get(key)

    def test_put_invalid_data(
        self,
        api_client: APIClient,
        fill_meal_batch: Callable,
    ) -> None:
        meals = fill_meal_batch()
        meal_id = meals[2].pk
        body = {
            'name': '',
            'price': '',
        }
        response = api_client.put(
            f'{ENDPOINT}{meal_id}/',
            json.dumps(body),
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestDeleteMeals:
    def test_delete_existent(
        self,
        api_client: APIClient,
        fill_meal_batch: Callable,
    ) -> None:
        meals = fill_meal_batch()
        meal_id = meals[2].pk
        response = api_client.delete(
            f'{ENDPOINT}{meal_id}/',
            content_type='application/json',
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Meal.objects.filter(pk=meal_id).exists()

    def test_delete_non_existent(
        self,
        api_client: APIClient,
    ) -> None:
        response = api_client.delete(f'{ENDPOINT}101/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

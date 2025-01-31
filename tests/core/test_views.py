from collections.abc import Callable
from http import HTTPStatus

from core.views import PageNotFoundView
from django.test import RequestFactory


class TestPageNotFoundView:
    @property
    def _view(self) -> Callable:
        return PageNotFoundView.as_view()

    def test_get(self, rf: RequestFactory) -> None:
        response = self._view(rf.get('/non-exists-page/'))
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert 'core/404.html' in response.template_name

from typing import Any

from core.constants import OrderStatus
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic.edit import ImproperlyConfigured


class DispatchUpdateDeleteViewMixin:
    """Миксин для обработки запросов к представлению.

    Attributes:
        warning_message: Текст предупреждения.
    """

    success_url = None
    warning_message = None

    def _check_attributes(self) -> None:
        """Проверяет, что определены необходимые аттрибуты.

        Raises:
            ImproperlyConfigured:
                Если не определен хотябы один аттрибут 'success_url'
                или 'warning_message'.
        """
        if not self.success_url:
            raise ImproperlyConfigured(
                f'{type(self).__name__} is missing a URL. Define '
                f'{type(self).__name__}.success_url.'
            )
        if not self.warning_message:
            raise ImproperlyConfigured(
                f'{type(self).__name__} is missing a message. Define '
                f'{type(self).__name__}.warning_message.'
            )

    def dispatch(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Any,
    ) -> HttpResponse:
        """Обрабатывает запрос к представлению.

        Если заказ имеет статус `OrderStatus.PAID_FOR`, то выводится
        соответствующее предупреждение, и происходит перенаправление на
        страницу успеха.

        Args:
            request: объект запроса HTTP
            args: Дополнительные позиционные параметры.
            kwargs: Дополнительные именованные параметры.

        Returns:
            Ответ на запрос.
        """
        self._check_attributes()
        if self.get_object().status == OrderStatus.PAID_FOR:
            messages.warning(request, self.warning_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

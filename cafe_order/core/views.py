from http import HTTPStatus
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic import TemplateView


class PageNotFoundView(TemplateView):
    """Представление для обработки ошибки 404.

    Attributes:
        template_name: Шаблон для отображения ответа.
    """

    template_name = 'core/404.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Добавляет путь текущего запроса в контекст данных.

        Args:
            **kwargs: Дополнительные аргументы контекста.

        Returns:
            Контекст данных с добавлением пути текущего запроса.
        """
        context = super().get_context_data(**kwargs)
        context['path'] = self.request.path
        return context

    def render_to_response(
        self,
        context: dict[str, Any],
        **response_kwargs: Any,
    ) -> TemplateResponse:
        """Возвращает ответ с шаблоном.

        Устанавливает статус ответа на 404 и вызывает родительский метод для
        рендера ответа.

        Args:
            context: Контекст данных для рендеринга шаблона.
            **response_kwargs: Дополнительные аргументы.

        Returns:
            Ответ с установленным статусом 404.
        """
        response_kwargs.setdefault('status', HTTPStatus.NOT_FOUND)
        return super().render_to_response(context, **response_kwargs)


class ServerErrorView(TemplateView):
    """Представление для обработки ошибки 500.

    Attributes:
        template_name: Шаблон для отображения ответа.
    """

    template_name = 'core/500.html'

    def render_to_response(
        self,
        context: dict[str, Any],
        **response_kwargs: Any,
    ) -> TemplateResponse:
        """Возвращает ответ с шаблоном.

        Устанавливает статус ответа на 500 и вызывает родительский метод для
        рендера ответа.

        Args:
            context: Контекст данных для рендеринга шаблона.
            **response_kwargs: Дополнительные аргументы.

        Returns:
            Ответ с установленным статусом 500.
        """
        response_kwargs.setdefault('status', HTTPStatus.INTERNAL_SERVER_ERROR)
        return super().render_to_response(context, **response_kwargs)


class PermissionDeniedView(TemplateView):
    """Представление для обработки ошибки 403.

    Attributes:
        template_name: Шаблон для отображения ответа.
    """

    template_name = 'core/403.html'

    def render_to_response(
        self,
        context: dict[str, Any],
        **response_kwargs: Any,
    ) -> TemplateResponse:
        """Возвращает ответ с шаблоном.

        Устанавливает статус ответа на 403 и вызывает родительский метод для
        рендера ответа.

        Args:
            context: Контекст данных для рендеринга шаблона.
            **response_kwargs: Дополнительные аргументы.

        Returns:
            Ответ с установленным статусом 403.
        """
        response_kwargs.setdefault('status', HTTPStatus.FORBIDDEN)
        return super().render_to_response(context, **response_kwargs)


def csrf_failure(request: HttpRequest, reason: str = '') -> HttpResponse:
    """Обработчик отказа CSRF-токена.

    Args:
        request: Запрос, вызвавший ошибку.
        reason: Причина отказа.

    Returns:
        Ответ с отображенной страницей ошибки.
    """
    return render(request, 'core/403csrf.html')

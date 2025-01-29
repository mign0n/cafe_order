from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    View,
)

from order import forms, mixins, models


class MealsCreateView(CreateView):
    """Представление для создания нового блюда.

    Attributes:
        model: Модель блюда.
        form_class: Форма для создания блюда.
        success_url: URL для перенаправления после успешного создания.
        template_name: Шаблон для отображения формы.
    """

    model = models.Meal
    form_class = forms.MealForm
    success_url = reverse_lazy('order:meal')
    template_name = 'order/meal_create.html'


class OrderCreateView(CreateView):
    """Представление для создания нового заказа.

    Attributes:
        model: Модель заказа.
        form_class: Форма для создания заказа.
        success_url: URL для перенаправления после успешного создания.
        template_name: Шаблон для отображения формы.
    """

    model = models.Order
    form_class = forms.OrderForm
    success_url = reverse_lazy('order:order')
    template_name = 'order/order_create.html'


class OrderDeleteView(mixins.DispatchUpdateDeleteViewMixin, DeleteView):
    """Представление для удаления существующего заказа.

    Attributes:
        model: Модель заказа.
        success_url: URL для перенаправления после успешного удаления.
    """

    model = models.Order
    success_url = reverse_lazy('order:order_list')
    warning_message = 'Deleting a paid order is prohibited.'


class OrderListView(ListView):
    """Представление для списка заказов.

    Attributes:
        model: Модель заказа.
        template_name: Шаблон для отображения списка.
        form_class: Форма для поиска заказов.
    """

    model = models.Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    form_class = forms.SearchOrderForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        """Фильтрует список заказов на основе данных формы.

        Args:
            request: Объект HTTP-запроса.

        Returns:
            Ответ с HTML-контентом страницы.
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            filters = {}
            if data.get('table_number'):
                filters['table_number'] = data['table_number']
            if data.get('status'):
                filters['status'] = data['status']
            queryset = self.model.objects.filter(**filters)
        else:
            queryset = self.model.objects.none()
        return render(
            request,
            self.template_name,
            self.get_context_data(
                form=form,
                object_list=queryset,
            ),
        )


class OrderUpdateView(mixins.DispatchUpdateDeleteViewMixin, UpdateView):
    """Представление для обновления статуса заказа.

    Attributes:
        model: Модель заказа.
        fields: Поля заказа для обновления.
        success_url: URL для перенаправления после успешного обновления.
        template_name: Шаблон для отображения формы.
    """

    model = models.Order
    form_class = forms.OrderUpdateForm
    success_url = reverse_lazy('order:order_list')
    template_name = 'order/order_update.html'
    warning_message = 'Changing a paid order is prohibited.'

    def get_initial(self) -> dict[str, QuerySet]:
        initial = super().get_initial()
        initial['items'] = self.object.items.all()
        return initial


class CurrentDayRevenueView(View):
    """Представление для выручки за смену.

    Attributes:
        model: Модель заказа.
        template_name: Шаблон для отображения формы.
    """

    model = models.Order
    template_name = 'order/revenue.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """Возвращает шаблон со значением выручки на текущую дату.

        Args:
            request: Объект HTTP-запроса.

        Returns:
            Ответ с HTML-контентом страницы.
        """
        return render(
            request,
            self.template_name,
            {
                'revenue': self.model.objects.get_revenue_for_day().get(
                    'revenue_per_shift',
                    {},
                ),
            },
        )

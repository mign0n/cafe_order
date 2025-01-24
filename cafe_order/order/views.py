from django.db.models import Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import datetime
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    View,
)

from order import forms, models
from order.constants import OrderStatus


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


class OrderDeleteView(DeleteView):
    """Представление для удаления существующего заказа.

    Attributes:
        model: Модель заказа.
        success_url: URL для перенаправления после успешного удаления.
    """

    model = models.Order
    success_url = reverse_lazy('order:order_list')


class OrderListView(ListView):
    """Представление для списка заказов.

    Attributes:
        model: Модель заказа.
        template_name: Шаблон для отображения списка.
        form_class: Форма для поиска заказов.
    """

    model = models.Order
    template_name = 'order/order_list.html'
    form_class = forms.SearchOrderForm

    def get(self, request: HttpRequest) -> HttpResponse:
        """Возвращает шаблон с формой поиска и всеми заказами.

        Args:
            request: Объект HTTP-запроса.

        Returns:
            Ответ с HTML-контентом страницы.
        """
        return render(
            request,
            self.template_name,
            {'form': self.form_class(), 'orders': self.model.objects.all()},
        )

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
            table_number = data.get('table_number')
            status = data.get('status')

            filters = {}
            if table_number:
                filters['table_number'] = table_number
            if status:
                filters['status'] = status

            orders = self.model.objects.filter(**filters)
        else:
            orders = self.model.objects.none()

        return render(
            request,
            self.template_name,
            {'form': form, 'orders': orders},
        )


class OrderUpdateView(UpdateView):
    """Представление для обновления статуса заказа.

    Attributes:
        model: Модель заказа.
        fields: Поля заказа для обновления.
        success_url: URL для перенаправления после успешного обновления.
        template_name: Шаблон для отображения формы.
    """

    model = models.Order
    fields = ('status',)
    success_url = reverse_lazy('order:order_list')
    template_name = 'order/order_update.html'


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
            {'revenue': self.model.objects.filter(
                status=OrderStatus.PAID_FOR,
                created_at__date=datetime.now().date(),
                ).annotate(total_price=Sum('items__price'))
                    .aggregate(
                        sum_of_total_prices=Sum('total_price'),
                    )['sum_of_total_prices'] or 0
            },
        )

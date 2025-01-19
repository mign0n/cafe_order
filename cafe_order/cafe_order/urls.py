from django.apps import apps
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        '',
        include(
            'order.urls',
            namespace=apps.get_app_config('order').name,
        ),
        name='index',
    ),
    path('admin/', admin.site.urls),
]

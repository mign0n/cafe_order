from core.views import (
    PageNotFoundView,
    PermissionDeniedView,
    ServerErrorView,
)
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
    path('api/', include('api.urls', namespace='api')),
    path('admin/', admin.site.urls),
]

handler404 = PageNotFoundView.as_view()
handler500 = ServerErrorView.as_view()
handler403 = PermissionDeniedView.as_view()

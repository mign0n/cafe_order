from django.urls import include, path

app_name = '%(app_label)s'

urlpatterns = [
    path('v1/', include('api.urls.v1'), name='v1'),
]

from rest_framework.authtoken import views as rest_views
from django.urls import path
from . import views

app_name = 'api'
version = 'v1'
urlpatterns = [
    path(f'{version}/auth/login', rest_views.obtain_auth_token, name='login'),
    path(f'{version}/auth/register', views.register, name='register'),
    path(f'{version}/booking', views.booking, name='booking'),
    path(f'{version}/transfers', views.transfer, name='history'),
]

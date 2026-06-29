from django.urls import path
from . import views

app_name = 'transfers'
urlpatterns = [
    path('', views.history, name='history'),
    path('new/', views.transfer, name='new'),
]
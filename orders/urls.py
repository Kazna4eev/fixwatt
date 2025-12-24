# orders/urls.py

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('created/', views.order_created, name='order_created'),

    # AJAX URLS ДЛЯ НОВОЇ ПОШТИ
    path('api/nova_poshta/cities/', views.nova_poshta_search_cities, name='nova_poshta_cities'),
    path('api/nova_poshta/warehouses/', views.nova_poshta_get_warehouses, name='nova_poshta_warehouses'),

    path('admin/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'), # Якщо ви використовуєте адмінку
]
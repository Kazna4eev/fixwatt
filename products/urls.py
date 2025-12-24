from django.urls import path
from . import views


app_name = 'products'


urlpatterns = [
    # Головна сторінка
    path('', views.home, name='home'), 
    
    # Каталог (всі товари)
    path('catalog/', views.product_list, name='product_list'),
    
    # Товари по категорії (те, що викликало помилку)
    path('catalog/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    
    # Детальна сторінка товару
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Інформаційні сторінки
    path('payment/', views.payment, name='payment'),
    path('delivery/', views.delivery, name='delivery'),
]
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'products/catalog.html', context)


def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:4]
    latest_products = Product.objects.all().order_by('-created')[:4]

    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    return render(request, 'products/product_detail.html', context)


def payment(request):
    return render(request, 'products/payment.html')


def delivery(request):
    return render(request, 'products/delivery.html')


from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows products to be viewed.
    Supports filtering, searching and ordering.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # 1. Підключаємо інструменти фільтрації
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # 2. Налаштування точних фільтрів
    filterset_fields = ['category', 'is_featured']

    # 3. Налаштування пошуку (входження тексту)
    search_fields = ['name', 'description']

    # 4. Налаштування сортування
    ordering_fields = ['price', 'name']

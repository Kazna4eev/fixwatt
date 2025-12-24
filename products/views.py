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
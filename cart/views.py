from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse # <--- ДОДАНО HttpResponse для повноти
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )

        # ЛОГІКА AJAX/REDIRECT для cart_add
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Коректна відповідь для AJAX
            return JsonResponse({'status': 'ok', 'quantity': cart.__len__()})
        else:
            return redirect('cart:cart_detail')

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    # Форма для оновлення кількості
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )

    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    # 💥 НОВА ЛОГІКА ДЛЯ AJAX-ВИДАЛЕННЯ 💥
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Якщо це AJAX, повертаємо успішну JSON-відповідь.
        # JS-скрипт (cart_update.js) отримає це і оновить сторінку.
        return JsonResponse({'status': 'ok'})

    # Якщо це звичайний POST-запит (без JS), робимо стандартне перенаправлення.
    return redirect('cart:cart_detail')
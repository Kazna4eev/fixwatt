from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_GET

from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .nova_poshta_service import nova_poshta_service
from .notifications import send_order_confirmation_email  # Імпорт функції

def order_create(request):
    cart = Cart(request)

    if not cart:
        return redirect('product_list')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user

            order.city_ref = form.cleaned_data.get('city_ref', '')
            order.warehouse_ref = form.cleaned_data.get('warehouse_ref', '')
            order.city_name = form.cleaned_data.get('city_name', '')
            order.warehouse_name = form.cleaned_data.get('warehouse_name', '')

            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()

            # === ВИПРАВЛЕНО ТУТ (ПРИБРАЛИ #) ===
            # Тепер функція спрацює і відправить лист (у консоль)
            send_order_confirmation_email(order) 
            # ===================================

            request.session['order_id'] = order.id
            return redirect(reverse('orders:order_created'))
    else:
        form = OrderCreateForm()

    return render(request,
                  'orders/create.html',
                  {'cart': cart, 'form': form})


def order_created(request):
    order_id = request.session.get('order_id')
    if order_id:
        try:
            order = Order.objects.get(id=order_id)

            if 'order_id' in request.session:
                del request.session['order_id']
            return render(request, 'orders/created.html', {'order': order})
        except Order.DoesNotExist:
            return redirect('product_list')
    return redirect('product_list')


# =========================================================================
# === AJAX ФУНКЦІЇ ДЛЯ НОВОЇ ПОШТИ  ===
# =========================================================================

@require_GET
def nova_poshta_search_cities(request):
    term = request.GET.get('term', '').strip()
    if not term or len(term) < 2:
        return JsonResponse({'cities': []})
    cities_data = nova_poshta_service.get_cities(term)
    cities = [{'ref': ref, 'description': desc} for ref, desc in cities_data]
    return JsonResponse({'cities': cities})


@require_GET
def nova_poshta_get_warehouses(request):
    """Отримує відділення Нової Пошти для заданого CityRef з фільтрацією."""
    city_ref = request.GET.get('city_ref', '').strip()
    term = request.GET.get('term', '').strip()

    if not city_ref:
        return JsonResponse({'warehouses': []})

    warehouses_data = nova_poshta_service.get_warehouses(city_ref, term=term)

    warehouses = [{'ref': ref, 'description': desc} for ref, desc in warehouses_data]

    return JsonResponse({'warehouses': warehouses})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})
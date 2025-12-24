import json
from decimal import Decimal
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse


from products.models import Product
from cart.cart import Cart
from .models import Order



class OrderCreationTests(TestCase):

    def setUp(self):
        self.client = Client()

        self.product1 = Product.objects.create(
            name='Тестовий Товар 1',
            slug='prod-1',
            price=Decimal('100.00')
        )
        self.product2 = Product.objects.create(
            name='Тестовий Товар 2',
            slug='prod-2',
            price=Decimal('200.00'),
            discount_price=Decimal('150.00')
        )

        self.valid_post_data = {
            'first_name': 'Тест',
            'last_name': 'Тестенко',
            'email': 'test@example.com',
            'phone': '123456789',
            'address': '',
            'city_name': 'Київ',
            'city_ref': '8d5a980d-391c-11dd-90d9-001a92567626',
            'warehouse_name': 'Відділення №1 (тест)',
            'warehouse_ref': '1ec09d88-e1c2-11e3-8c4a-0050568002cf',
        }

    def _setup_cart_in_session(self):
        """
        Допоміжна функція для додавання товарів у сесію тестового клієнта (self.client).
        """
        session = self.client.session
        request_for_cart = RequestFactory().get('/')
        request_for_cart.session = session

        cart = Cart(request_for_cart)
        cart.add(self.product1, quantity=2)
        cart.add(self.product2, quantity=1)
        cart.save()

        # === КРИТИЧНЕ ВИПРАВЛЕННЯ: ЗБЕРІГАЄМО СЕСІЮ В КЛІЄНТІ ===
        session.save()
        # ========================================================

    def test_order_create_view_get_with_cart(self):
        """Тест: GET-запит до /orders/create/ з повним кошиком."""

        self._setup_cart_in_session()  # Тепер кошик не порожній

        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)  # Тепер має бути 200
        self.assertIn('form', response.context)

    def test_order_create_view_redirects_if_cart_empty(self):
        """Тест: /orders/create/ має перенаправляти, якщо кошик порожній."""
        response = self.client.get(reverse('orders:order_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('product_list'))

    def test_order_create_view_post_invalid_form(self):
        """Тест: POST-запит з невалідною формою (порожнє ім'я)."""

        self._setup_cart_in_session()  # Тепер кошик не порожній

        invalid_data = self.valid_post_data.copy()
        invalid_data['first_name'] = ''

        response = self.client.post(reverse('orders:order_create'), data=invalid_data)

        self.assertEqual(response.status_code, 200)  # Очікуємо 200
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_create_view_post_success(self):
        """
        ГОЛОВНИЙ ТЕСТ: Успішне створення замовлення.
        """

        self._setup_cart_in_session()  # Тепер кошик не порожній

        response = self.client.post(reverse('orders:order_create'), data=self.valid_post_data)

        # 1. Перевіряємо, що створено 1 замовлення
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()

        # 2. Перевіряємо деталі
        self.assertEqual(order.first_name, 'Тест')
        self.assertEqual(order.city_ref, '8d5a980d-391c-11dd-90d9-001a92567626')

        # 3. Перевіряємо елементи замовлення
        self.assertEqual(order.items.count(), 2)

        # 4. Перевіряємо загальну суму (100*2 + 150*1 = 350)
        self.assertEqual(order.get_total_cost(), Decimal('350.00'))

        # 5. Перевіряємо, що кошик очищено
        # Отримуємо сесію *після* POST-запиту
        session_after_order = self.client.session
        request_after = RequestFactory().get('/')
        request_after.session = session_after_order
        cart_after_order = Cart(request_after)
        self.assertEqual(len(cart_after_order), 0)

        # 6. Перевіряємо перенаправлення
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orders:order_created'))

    def test_ajax_get_cities_from_json(self):
        """Тест: чи працює AJAX-view для міст (читання з data/cities.json)."""

        response = self.client.get(
            reverse('orders:nova_poshta_cities'),
            data={'term': 'Київ'},  # Використовуємо 'Київ' з вашого cities.json
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )

        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)

        self.assertIn('cities', content)
        # Перевіряємо, що знайшли Київ (використовуємо 'description' з вашої view)
        self.assertTrue(any(city['description'] == 'Київ' for city in content['cities']))
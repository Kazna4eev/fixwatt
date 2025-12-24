from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware

from products.models import Product
from .cart import Cart


class CartTests(TestCase):

    def setUp(self):
        """
        Ця функція запускається перед кожним тестом.
        Вона створює необхідні об'єкти (товари, запит, кошик).
        """

        # Створюємо два товари для тестів
        self.product1 = Product.objects.create(
            name='Товар 1 (без знижки)',
            slug='product-1',
            price=Decimal('100.00')
        )
        self.product2 = Product.objects.create(
            name='Товар 2 (зі знижкою)',
            slug='product-2',
            price=Decimal('200.00'),
            discount_price=Decimal('150.00')  # Цей товар має знижку
        )

        # Нам потрібен об'єкт 'request' з сесією, щоб ініціалізувати кошик.
        # Ми використовуємо RequestFactory для створення "штучного" запиту.
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        # Додаємо до запиту middleware для сесій (щоб self.request.session працював)
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(self.request)
        self.request.session.save()

        # Нарешті, ініціалізуємо кошик
        self.cart = Cart(self.request)

    def test_add_new_product(self):
        """Тест: додавання нового товару в кошик."""
        self.cart.add(product=self.product1, quantity=1)

        # Перевіряємо, що в кошику 1 товар
        self.assertEqual(len(self.cart), 1)
        # Перевіряємо, що ID товару є ключем у словнику кошика
        self.assertIn(str(self.product1.id), self.cart.cart)
        # Перевіряємо кількість
        self.assertEqual(self.cart.cart[str(self.product1.id)]['quantity'], 1)

    def test_add_existing_product(self):
        """Тест: додавання товару, що вже є в кошику (збільшення кількості)."""
        self.cart.add(product=self.product1, quantity=1)  # Додали 1
        self.cart.add(product=self.product1, quantity=2)  # Додали ще 2

        # Загальна кількість має бути 3
        self.assertEqual(len(self.cart), 3)
        self.assertEqual(self.cart.cart[str(self.product1.id)]['quantity'], 3)

    def test_cart_uses_regular_price(self):
        """Тест: кошик має використовувати звичайну ціну, якщо немає знижки."""
        self.cart.add(product=self.product1, quantity=1)

        self.assertEqual(self.cart.cart[str(self.product1.id)]['price'], '100.00')
        self.assertEqual(self.cart.get_total_price(), Decimal('100.00'))

    def test_cart_uses_discount_price(self):
        """Тест: кошик має використовувати ЦІНУ ЗІ ЗНИЖКОЮ, якщо вона є."""
        self.cart.add(product=self.product2, quantity=1)

        # Перевіряємо, що в кошик збереглася саме ціна зі знижкою
        self.assertEqual(self.cart.cart[str(self.product2.id)]['price'], '150.00')
        self.assertEqual(self.cart.get_total_price(), Decimal('150.00'))

    def test_get_total_price_complex(self):
        """Тест: розрахунок загальної суми для кількох різних товарів."""
        self.cart.add(product=self.product1, quantity=2)  # 2 * 100.00 = 200.00
        self.cart.add(product=self.product2, quantity=1)  # 1 * 150.00 = 150.00

        # 200.00 + 150.00 = 350.00
        self.assertEqual(self.cart.get_total_price(), Decimal('350.00'))

    def test_remove_product(self):
        """Тест: видалення товару з кошика."""
        self.cart.add(product=self.product1, quantity=3)
        self.cart.add(product=self.product2, quantity=1)

        self.cart.remove(self.product1)  # Видаляємо перший товар

        # Перевіряємо, що залишився лише другий
        self.assertEqual(len(self.cart), 1)
        self.assertNotIn(str(self.product1.id), self.cart.cart)
        self.assertIn(str(self.product2.id), self.cart.cart)

    def test_clear_cart(self):
        """Тест: повне очищення кошика."""
        self.cart.add(product=self.product1, quantity=1)
        self.cart.add(product=self.product2, quantity=1)

        self.cart.clear()

        # Перевіряємо, що словник кошика в сесії порожній
        self.assertEqual(len(self.cart.cart), 0)
        # Перевіряємо, що ключ 'cart' видалено з сесії
        self.assertIsNone(self.request.session.get(settings.CART_SESSION_ID))
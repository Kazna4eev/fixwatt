from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from .models import Product


class ProductModelTests(TestCase):

    def setUp(self):
        """Створюємо тестові продукти."""
        self.product_regular = Product.objects.create(
            name='Товар без знижки',
            slug='product-regular',
            price=Decimal('100.00'),
            is_featured=False
        )
        self.product_discounted = Product.objects.create(
            name='Товар зі знижкою',
            slug='product-discounted',
            price=Decimal('200.00'),
            discount_price=Decimal('150.00'),
            is_featured=True
        )

    def test_product_creation(self):
        """Тест: чи правильно створено товар."""
        self.assertEqual(self.product_regular.name, 'Товар без знижки')
        self.assertEqual(self.product_regular.price, Decimal('100.00'))
        self.assertFalse(self.product_regular.is_featured)

    def test_get_absolute_url(self):
        """Тест: чи правильно генерується URL товару."""
        expected_url = f'/{self.product_regular.slug}/'
        self.assertEqual(self.product_regular.get_absolute_url(), expected_url)

    # === Тести для нашої нової логіки знижок ===

    def test_get_display_price_no_discount(self):
        """Тест: get_display_price має повертати звичайну ціну."""
        self.assertEqual(self.product_regular.get_display_price, Decimal('100.00'))

    def test_get_display_price_with_discount(self):
        """Тест: get_display_price має повертати ціну зі знижкою."""
        self.assertEqual(self.product_discounted.get_display_price, Decimal('150.00'))


class ProductViewTests(TestCase):

    def setUp(self):
        """Створюємо тестові продукти для перевірки 'views'."""
        self.featured_product = Product.objects.create(
            name='Рекомендований',
            slug='featured',
            price=10,
            is_featured=True  # Позначено як рекомендований
        )
        self.regular_product = Product.objects.create(
            name='Звичайний',
            slug='regular',
            price=20,
            is_featured=False  # Не рекомендований
        )

    def test_product_list_view_context(self):
        """Тест: чи правильно view 'product_list' розділяє товари."""

        # Робимо запит до головної сторінки
        response = self.client.get(reverse('product_list'))

        # Перевіряємо, що сторінка завантажилась (статус 200)
        self.assertEqual(response.status_code, 200)

        # Перевіряємо контекст (дані, які view передає у шаблон)

        # Чи є 'featured_products' у контексті і чи містить він наш товар?
        self.assertIn('featured_products', response.context)
        self.assertIn(self.featured_product, response.context['featured_products'])
        self.assertNotIn(self.regular_product, response.context['featured_products'])

        # Чи є 'regular_products' у контексті і чи містить він наш товар?
        self.assertIn('regular_products', response.context)
        self.assertIn(self.regular_product, response.context['regular_products'])
        self.assertNotIn(self.featured_product, response.context['regular_products'])
from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    """
    Клас Кошика, що зберігається у сесії.
    """

    def __init__(self, request):
        """
        Ініціалізувати кошик.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Зберегти порожній кошик у сесії
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Додати товар у кошик або оновити його кількість, враховуючи знижку.
        """
        product_id = str(product.id)

        # ВИЗНАЧАЄМО АКТУАЛЬНУ ЦІНУ
        if product.discount_price:
            actual_price = product.discount_price
        else:
            actual_price = product.price

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(actual_price)}  # <-- ВИПРАВЛЕНО

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # Позначити сесію як "змінену", щоб вона збереглася
        self.session.modified = True

    def remove(self, product):
        """
        Видалити товар із кошика.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Ітеруватися по елементах кошика та отримувати товари з бази даних.
        """
        product_ids = self.cart.keys()
        # Отримати об'єкти Product
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Повернути загальну кількість елементів у кошику.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Повернути загальну вартість товарів у кошику.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Очищуємо локальний словник (який перевіряє тест)
        self.cart = {}

        # Видаляємо ключ із сесії Django
        if settings.CART_SESSION_ID in self.session:
            del self.session[settings.CART_SESSION_ID]

        self.save()
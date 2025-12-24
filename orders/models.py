from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Очікує'),
        ('accepted', 'Прийняте'),
        ('shipped', 'Відправлене'),
        ('completed', 'Оплачено / Завершено'),
        ('canceled', 'Скасовано'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders', verbose_name="Користувач")
    first_name = models.CharField(max_length=50, verbose_name="Ім'я")
    last_name = models.CharField(max_length=50, verbose_name="Прізвище")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон", default='')
    address = models.CharField(max_length=250, blank=True, null=True, verbose_name="Адреса доставки")


    city = models.CharField(max_length=100, verbose_name="Місто (старе)", blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    paid = models.BooleanField(default=False, verbose_name="Оплачено")

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Статус замовлення"
    )

    ttn = models.CharField(max_length=50, blank=True, null=True, verbose_name="ТТН Нова Пошта")


    city_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Місто (НП)")
    city_ref = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ref Міста (НП)")
    warehouse_name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Відділення (НП)")
    warehouse_ref = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ref Відділення (НП)")



    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"

    def __str__(self):
        return f'Замовлення {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
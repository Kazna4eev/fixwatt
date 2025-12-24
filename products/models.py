from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # Переконайтеся, що у вас в urls.py є name='product_list_by_category'
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Категорія"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    

    created = models.DateTimeField(auto_now_add=True)
    

    updated = models.DateTimeField(auto_now=True)


    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Ціна зі знижкою"
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="Рекомендований товар"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.slug])

    @property
    def get_display_price(self):
        """
        Повертає ціну зі знижкою, якщо вона існує,
        інакше повертає звичайну ціну.
        """
        if self.discount_price:
            return self.discount_price
        return self.price
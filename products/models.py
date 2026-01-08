from django.db import models
from django.urls import reverse
from PIL import Image

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
    sku = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name="Артикул (SKU)")
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 800:
                output_size = (800, 600)
                img.thumbnail(output_size)
                img.save(self.image.path)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True, null=True, verbose_name="Опис (Alt text)")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 800:
                output_size = (800, 600)
                img.thumbnail(output_size)
                img.save(self.image.path)
    
    class Meta:
        verbose_name = "Додаткове фото"
        verbose_name_plural = "Додаткові фото"

class SiteBanner(models.Model):
    BANNER_TYPES = (
        ('info', 'Information (Blue)'),
        ('warning', 'Warning (Yellow)'),
        ('danger', 'Critical (Red)'),
        ('success', 'Success (Green)'),
    )

    text = models.CharField(max_length=255, verbose_name="Текст банера")
    is_active = models.BooleanField(default=True, verbose_name="Активний")
    banner_type = models.CharField(
        max_length=20, 
        choices=BANNER_TYPES, 
        default='info', 
        verbose_name="Тип (Колір)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_banner_type_display()}: {self.text[:50]}"

    class Meta:
        verbose_name = "Глобальний Банер"
        verbose_name_plural = "Глобальні Банери"
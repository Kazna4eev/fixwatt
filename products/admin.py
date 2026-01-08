from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from .models import Product, Category, ProductImage
from django.utils.text import slugify

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# Inline class for additional images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# 1. Описуємо правила імпорту (Resource)
class ProductResource(resources.ModelResource):
    # Це магія для категорій:
    # Ми кажемо: "Шукай категорію по полю 'name' (назва), а не по ID"
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    def before_import_row(self, row, **kwargs):
        """
        Автоматична генерація slug, якщо його немає в Excel.
        """
        if 'slug' not in row or not row['slug']:
            # Генеруємо slug з назви товару (підтримка кирилиці)
            row['slug'] = slugify(row.get('name', ''), allow_unicode=True)

    class Meta:
        model = Product
        # Які поля шукати в Excel (назви колонок мають співпадати!)
        fields = ('id', 'sku', 'name', 'slug', 'description', 'price', 'category', 'image')
        # Яке поле унікальне (щоб не створювати дублікати, а оновлювати існуючі)
        import_id_fields = ('sku',)

# 2. Підключаємо це до адмінки
@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    inlines = [ProductImageInline]
    
    # Зберігаємо існуючі налаштування адмінки
    list_display = ('name', 'sku', 'category', 'price', 'discount_price', 'is_featured', 'created')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_featured', 'category', 'created', 'updated')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'product', 'alt_text']

from .models import SiteBanner
@admin.register(SiteBanner)
class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ('text', 'banner_type', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active', 'banner_type')
    ordering = ('-created_at',)
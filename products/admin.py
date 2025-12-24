from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('name', 'category', 'price', 'discount_price', 'is_featured', 'created')
    
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'discount_price', 'is_featured']
    list_filter = ('is_featured', 'category', 'created', 'updated')
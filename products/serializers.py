from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 
                  'discount_price', 'image', 'category', 'is_featured', 
                  'get_display_price', 'get_absolute_url']

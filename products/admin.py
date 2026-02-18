from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'gender', 'product_type', 'quantity')
    prepopulated_fields = {'slug': ('name',)}



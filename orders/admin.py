from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity')
    list_filter = ('product',)


# from django.contrib import admin
# from .models import Cart

# class CartAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_at')

# admin.site.register(Cart, CartAdmin)

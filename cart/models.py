from django.db import models
from django.conf import settings
from products.models import Product
from accounts.models import Customer


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user.email}"

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all()) # used a concept in python called Generator Expression
    
        # the casual method to do the above calculation 

        # def total_price(self):
        #     total = 0
        #     items = self.items.all()

        #     for item in items:
        #         total = total + item.subtotal()

        #     return total


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

    def subtotal(self):
        return self.product.price * self.quantity

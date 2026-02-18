from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

@login_required
def decrease_quantity(request, id):
    item = get_object_or_404(CartItem, id=id, cart__user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})


@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(CartItem, id=id, cart__user=request.user)   
    item.delete()
    return redirect('view_cart')

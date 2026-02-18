from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from cart.models import Cart
from .models import Order, OrderItem


# 1️ CHECKOUT (Only collect address)
@login_required
def checkout_view(request):

    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('view_cart')

    if request.method == "POST":

        address = request.POST.get("address")
        phone = request.POST.get("phone")

        # Save temporarily in session
        request.session['checkout_data'] = {
            'address': address,
            'phone': phone
        }

        return redirect('payment_page')

    return render(request, 'orders/checkout.html', {'cart': cart})


# 2️ PAYMENT PAGE (Dummy)
@login_required
def payment_page(request):

    cart = get_object_or_404(Cart, user=request.user)

    if request.method == "POST":
        return redirect('payment_success')

    return render(request, 'orders/payment.html', {'cart': cart})


# 3️ PAYMENT SUCCESS → CREATE ORDER + REDUCE STOCK
@login_required
@transaction.atomic
def payment_success(request):

    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('product').select_for_update()

    checkout_data = request.session.get('checkout_data')

    if not checkout_data:
        return redirect('checkout')

    # CHECK STOCK
    for item in cart_items:
        if item.quantity > item.product.quantity:
            messages.error(
                request,
                f"Not enough stock for {item.product.name}"
            )
            return redirect('view_cart')

    # CREATE ORDER
    order = Order.objects.create(
        user=request.user,
        total_amount=cart.total_price(),
        shipping_address=checkout_data['address'],
        phone_number=checkout_data['phone']
    )

    # CREATE ORDER ITEMS + REDUCE STOCK
    for item in cart_items:
        product = item.product
        product.quantity -= item.quantity
        product.save()

        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=item.quantity
        )

    # CLEAR CART
    cart_items.delete()
    del request.session['checkout_data']

    return redirect('order_success', order.id)


# 4️ ORDER SUCCESS
@login_required
def order_success(request, id):

    order = get_object_or_404(Order, id=id, user=request.user)

    return render(request, 'orders/order_success.html', {'order': order} )

@login_required
def order_history(request):

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'orders/order_history.html', {
        'orders': orders
    })

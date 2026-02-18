from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('payment/', views.payment_page, name='payment_page'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('success/<int:id>/', views.order_success, name='order_success'),
    path('my-orders/', views.order_history, name='order_history'),

]

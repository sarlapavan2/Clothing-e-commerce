from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('explore/', views.explore_range, name='explore'),
    path('men/', views.men_products, name='men'),
    path('women/', views.women_products, name='women'),
    path('search/', views.search_products, name='search_products'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    
]

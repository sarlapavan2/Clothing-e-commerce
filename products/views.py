from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# 1️ Explore Range – ALL products
@login_required
def explore_range(request):
    context = {
        'hoodies': Product.objects.filter(product_type='HOODIE'),
        'jackets': Product.objects.filter(product_type='JACKET'),
        'shirts': Product.objects.filter(product_type='SHIRT'),
        'pants': Product.objects.filter(product_type='PANT'),
    }
    return render(request, 'products/explore_range.html', context)


# 2️ Men Products
@login_required
def men_products(request):
    products = Product.objects.filter(gender='M')
    return render(request, 'products/men.html', {'products': products})


# 3️ Women Products
@login_required
def women_products(request):
    products = Product.objects.filter(gender='F')
    return render(request, 'products/women.html', {'products': products})



@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {
        'product': product
    })


@login_required
def search_products(request):

    query = request.GET.get('q')
    gender = request.GET.get('gender')
    category = request.GET.get('category')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if gender:
        products = products.filter(gender=gender)

    if category:
        products = products.filter(product_type=category)

    context = {
        'products': products,
        'query': query,
        'selected_gender': gender,
        'selected_category': category,
    }

    return render(request, 'products/search_results.html', context)

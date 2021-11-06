from django.shortcuts import render, get_object_or_404

from .models import FeaturedProduct
from shop.models import Category, Product, ProductReview

# Create your views here.

def index(request):
    products_of_categories = []
    category_product = Product.objects.all()[:21].values('category', 'id')
    categories = {item['category'] for item in category_product}

    # Appending each category wise product
    for category in categories:
        products = Product.objects.filter(category=category)[:5]
        products_of_categories.append(products)

    context = {
        'featured': FeaturedProduct.objects.all()[:3],
        'products_of_categories': products_of_categories,
    }
    return render(request, 'home/index.html', context)

def category(request, category):
    category_obj = get_object_or_404(Category, name=category)
    context = {
        'category': category_obj,
    }
    return render(request, 'home/category.html', context)
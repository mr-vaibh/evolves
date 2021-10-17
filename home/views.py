from django.shortcuts import render, get_object_or_404

from .models import FeaturedProduct
from shop.models import Category, Product, ProductReview

# Create your views here.

def index(request):
    # # get 3 random categories
    # random_categories = Category.objects.order_by('?')[:3]
    # print(random_categories)

    # # List of Products' Queryset of random categories
    # product_of_categories = [
    #     Product.objects.filter(category=random_categories[n])
    #     for n in range(random_categories.count())
    #     if Product.objects.filter(category=random_categories[n]).count() != 0
    # ]
    # print(product_of_categories)

    products_of_categories = []
    category_product = Product.objects.all()[:21].values('category', 'id')
    categories = {item['category'] for item in category_product}

    # Appending each category wise product
    for category in categories:
        products = Product.objects.filter(category=category)[:5]
        products_of_categories.append(products)
    print(products_of_categories)

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
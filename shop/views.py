from django.shortcuts import render, get_object_or_404

from .models import Product, ProductReview

# Create your views here.

def product_detail(request, slug):
    context = {
        'product': get_object_or_404(Product, slug=slug),
        'product_reviews': ProductReview.objects.filter(product__slug=slug)
    }
    return render(request, 'shop/product_detail.html', context)


def search(request, query):
    context = {
        'query': query,
        'products': Product.objects.filter(name__icontains=query)
        .union(Product.objects.filter(category__name__icontains=query))
        .union(Product.objects.filter(sub_category__name__icontains=query))
        .order_by('-created_at')
    }
    return render(request, 'shop/search.html', context)
from json.encoder import JSONEncoder
from django import forms
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User
from account.models import UserProfile
from .models import Product, ProductReview
from .forms import UpdateCartForm
from django.db.models import Avg

# Create your views here.

def product_detail(request, slug):
    form = UpdateCartForm()
    product = get_object_or_404(Product, slug=slug)

    product_medias = [product.image1, product.image2, product.image3, product.image4, product.image5, product.image6, product.video]
    product_medias = [media for media in product_medias if media]
    
    product_reviews = ProductReview.objects.filter(product__slug=slug)

    # very ugly approach to handle stars
    avg_stars = product_reviews.aggregate(Avg('stars'))['stars__avg']
    avg_stars = 2.6
    half_star = int(str(avg_stars)[-1]) > 5

    import json
    product.features = json.dumps(product.features)

    context = {
        'form': form,
        'product': product,
        'product_medias': product_medias,
        'product_reviews': product_reviews,
        'avg_stars': avg_stars,
        'filled_stars': range(round(avg_stars)),
        'half_star': half_star,
        'unfilled_stars': range(5 - round(avg_stars)),
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


def get_cart(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            import json
            cartString = request.user.userprofile.cart

            data = {'cart': json.loads(cartString), 'loggedin': True}
        else:
            data = {'cart': None, 'loggedin': False}
    return JsonResponse(data)


def update_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = UpdateCartForm(request.POST, instance=request.user)
            if form.is_valid():
                import json
                
                cleaned_cart_data = form.cleaned_data['cart']

                # convert to JSON
                cart_obj = json.loads(cleaned_cart_data)

                # To find for duplicate product and just update the value
                for product in cart_obj[:-1]:
                    if product['id'] == cart_obj[-1]['id']:
                        product['quantity'] = cart_obj[-1]['quantity']
                        cart_obj.pop()
                        break

                # convert to STRING
                cleaned_cart_data = json.dumps(cart_obj)

                # update the object
                UserProfile.objects.filter(user=request.user).update(cart=cleaned_cart_data)
                form.save()
                data = {'loggedin': True}
        else:
            data = {'loggedin': False, 'localCart': request.POST.get('cart')}
    return JsonResponse(data)
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from account.models import UserProfile
from .models import Product, ProductReview, Order
from .forms import UpdateCartForm
from django.db.models import Avg

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# RAZORPAY logic credit: https://www.geeksforgeeks.org/razorpay-integration-in-django/

# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# Create your views here.

def product_detail(request, slug):
    form = UpdateCartForm()
    product = get_object_or_404(Product, slug=slug)

    product_medias = [product.image1, product.image2, product.image3, product.image4, product.image5, product.image6, product.video]
    product_medias = [media for media in product_medias if media]
    
    product_reviews = ProductReview.objects.filter(product__slug=slug)

    # very ugly approach to handle stars
    avg_stars = product_reviews.aggregate(Avg('stars'))['stars__avg']
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

                # check if duplicate product exists and just update the value if so
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


def delete_cart(request, product_id):
    if request.method == 'DELETE':
        if request.user.is_authenticated:
            import json
            
            cart = json.loads(request.user.userprofile.cart)

            for product in cart:
                if product['id'] == product_id:
                    cart.remove(product)
                    break

            cart = json.dumps(cart)

            # update the object
            UserProfile.objects.filter(user=request.user).update(cart=cart)
            data = {'loggedin': True}
        else:
            data = {'loggedin': False}
    return JsonResponse(data)


# THIS FUNCTION HANDLES THE `ORDER` when Buy button is clicked
@login_required
def order(request):
    user = request.user
    if user.userprofile.cart != '[]':
        if request.method == 'GET':
            # code to delete empty order
            order_id = request.GET.get('order_id')
            Order.objects.filter(razp_order_id=order_id).delete()
        elif request.method == 'POST':
            # Code to create an order
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            address = request.POST.get('address1') + ', ' + request.POST.get('address2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zip_code = int(request.POST.get('zip_code'))
            items = user.userprofile.cart
            razp_amount = int(request.POST.get('amount')) / 100 # amount in Rs.
            order_id = request.POST.get('order_id')

            order = Order(user=user, name=name, email=email, phone_no=phone_no,
                            address=address, city=city, state=state, zip_code=zip_code,
                            items=items, razp_amount=razp_amount, razp_order_id=order_id)
            order.save()
    return HttpResponse()


@login_required
def checkout(request):
    user = request.user

    # if user isn't authenticated or cart is empty
    if user.userprofile.cart == '[]':
        return redirect(reverse('account:login'))
    
    total_price = user.userprofile.total_price()

    currency = 'INR'
    amount = int(total_price * 100) #  money in integer (paise)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = '/paymenthandler/'
    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    context['auto_fill'] = {
        'name': user.userprofile.get_full_name() if user.userprofile.get_full_name() != ' ' else '',
        'email': user.email or '',
        'phone_no': user.userprofile.phone_no or '',
    }
    context['cart'] = user.userprofile.cart

    return render(request, 'shop/checkout.html', context)


@csrf_exempt
def callback(request):
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)

            order_object = Order.objects.filter(razp_order_id=razorpay_order_id)

            order_object.update(
                razp_payment_id=payment_id,
                razp_signature=signature,
            )
            
            if result is None:
                total_price = request.user.userprofile.total_price()
                amount = int(total_price * 100) #  money in integer (paise)
                try:
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    order_object.update(status='success')
                    UserProfile.objects.filter(user=request.user).update(cart='[]')

                    # render success page on successful caputre of payment
                    return render(request, 'shop/paymentsuccess.html', {'order': order_object.first()})
                except:
                    # if there is an error while capturing payment.
                    order_object.update(status='failure')
                    return render(request, 'shop/paymentfail.html', {'order': order_object.first()})
            else:
                # if signature verification fails.
                order_object.update(status='failure')
                return render(request, 'shop/paymentfail.html', {'order': order_object.first()})
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
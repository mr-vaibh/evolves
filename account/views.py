from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm

from shop.models import Order

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home:index')
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})


def cart(request):
    context = {}
    
    if request.user.is_authenticated:
        context['cart'] = request.user.userprofile.cart
    return render(request, 'account/cart.html', context)

@login_required
def my_orders(request):
    context = {
        'orders': Order.objects.filter(user=request.user).order_by('-datetime')
    }
    return render(request, 'account/myorders.html', context)

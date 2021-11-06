from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm


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
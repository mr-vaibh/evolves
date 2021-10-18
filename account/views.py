from django.shortcuts import render, redirect
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings

from django.views.generic import View

def cart():
    pass

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.errors)
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
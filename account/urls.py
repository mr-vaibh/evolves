from django.urls import path

from django.contrib.auth import views as auth_views
from . import views

app_name = 'account'
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('my-orders/', views.my_orders, name='myorders'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
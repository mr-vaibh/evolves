from django.urls import path

from . import views

app_name = 'account'
urlpatterns = [
    path('cart/', views.LoginView.as_view(), name='cart'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]

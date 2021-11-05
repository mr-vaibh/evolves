from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('product/<slug:slug>', views.product_detail, name='product_detail'),
    path('search/<str:query>/', views.search, name='search'),
    path('api/getcart/', views.get_cart, name='getcart'),
    path('api/updatecart/', views.update_cart, name='updatecart'),
]

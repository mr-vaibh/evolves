from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('product/<slug:slug>', views.product_detail, name='product_detail'),
    path('search/<str:query>/', views.search, name='search'),
    path('api/getcart/', views.get_cart, name='getcart'),
    path('api/updatecart/', views.update_cart, name='updatecart'),
    path('api/deletecart/<int:product_id>', views.delete_cart, name='deletecart'),
    path('api/order/', views.order, name='order'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymenthandler/', views.callback, name='callback'),
]

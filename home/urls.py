from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index),
    path('category/<str:category>/', views.category, name='category'),
]

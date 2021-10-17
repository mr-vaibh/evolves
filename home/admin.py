from django.contrib import admin

from .models import FeaturedProduct

# Register your models here.

@admin.register(FeaturedProduct)
class FeaturedProduct(admin.ModelAdmin):
    pass
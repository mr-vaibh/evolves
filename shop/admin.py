from django.contrib import admin

from .models import Category, SubCategory, Product, ProductReview

# Register your models here.
class ProductReviewAdmin(admin.TabularInline):
    model = ProductReview


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'excerpt', 'stocks', )
    search_fields = ('name', 'excerpt', )
    inlines = [ProductReviewAdmin]

    class Meta:
        model = Product

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'review', )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', )
    search_fields = ('name', 'category', )

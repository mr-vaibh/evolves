from django.contrib import admin

from .models import Category, SubCategory, Product, ProductReview, Order

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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'razp_order_id', 'status',)
    list_filter = ('status',)
    search_fields = ('user__username', 'user__email', 'user__userprofile__phone_no')
from django.db import models
from django.db.models.expressions import F

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from .validators import validate_video_size, validate_video_extension

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, default='')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey("shop.Category", verbose_name=_("Category"), on_delete=models.CASCADE)
    name = models.CharField(_("Sub Category"), max_length=100, default='')

    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'
    
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    added_by = models.ForeignKey(User, verbose_name=_("Product Added by"), on_delete=models.CASCADE, null=True)
    slug = models.SlugField(_("Slug"), default='', editable=False, max_length=255, null=False, unique=True)
    name = models.CharField(_("Product Name"), max_length=255, default='')
    category = models.ForeignKey("shop.Category", verbose_name=_("Category"), on_delete=models.CASCADE)
    sub_category = models.ForeignKey("shop.SubCategory", verbose_name=_("Sub-Category"), on_delete=models.CASCADE)
    excerpt = models.TextField(_("Short Description"), max_length=350, default='')
    description = models.TextField(_("Long Description"), max_length=5000, default='')
    price = models.DecimalField(_("Price (in Rupees)"), max_digits=10, decimal_places=2)
    discount = models.IntegerField(_("Discount (in percent)"), blank=True, null=True)
    stocks = models.IntegerField(_("Stocks Left"), blank=True, null=True)
    replacement = models.CharField(_("Replacement"), max_length=20, default='No', blank=True)
    features = models.JSONField(_("Product Features"), blank=True, null=True, encoder=None, decoder=None)
    image1 = models.ImageField(_("Image 1"), upload_to=f'product_images/', blank=False, null=True)
    image2 = models.ImageField(_("Image 2"), upload_to=f'product_images/', blank=True, null=True)
    image3 = models.ImageField(_("Image 3"), upload_to=f'product_images/', blank=True, null=True)
    image4 = models.ImageField(_("Image 4"), upload_to=f'product_images/', blank=True, null=True)
    image5 = models.ImageField(_("Image 5"), upload_to=f'product_images/', blank=True, null=True)
    image6 = models.ImageField(_("Image 6"), upload_to=f'product_images/', blank=True, null=True)
    video = models.FileField(
        upload_to=f'product_videos/',
        blank=True,
        null=True,
        validators=[
            validate_video_size,
            validate_video_extension
        ]
    )
    created_at = models.DateTimeField(_("Date & Time created"), auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(_("Date & Time updated"), auto_now=True)


    def __str__(self) -> str:
        return self.name
    
    def net_price_each(self):
        price = self.price
        discount = self.discount if self.discount else 0
        discounted_price = float(100 - discount)/100 * float(price)
        return discounted_price
    
    def save(self, *args, **kwargs):
        from django.template.defaultfilters import slugify
        from django.utils.crypto import get_random_string

        if not self.id:
            self.slug = slugify(self.name + '--' +
                                get_random_string(length=7))
        super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.video:
            self.video.delete()
            super().delete(*args, **kwargs)

class ProductReview(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Related User"), on_delete=models.CASCADE)
    product = models.ForeignKey("shop.Product", verbose_name=_("Related Product"), on_delete=models.CASCADE)
    review = models.TextField(_("Product Review"), max_length=500)
    stars = models.PositiveSmallIntegerField(_("Stars"), null=True)
    datetime = models.DateTimeField(_("Review Date & Time"), auto_now_add=True)

    def __str__(self) -> str:
        return self.review


class Order(models.Model):

    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failure', 'Failure'),
        ('pending', 'Pending'),
        ('refund', 'Refund'),
    ]
    
    user = models.ForeignKey(User, verbose_name=_("Related User"), on_delete=models.CASCADE)
    name = models.CharField(_("Order in name of"), max_length=100, default='', blank=False)
    email = models.EmailField(_("Email"), blank=True, max_length=254)
    phone_no = models.PositiveIntegerField(_("Phone Number"), blank=True, null=True)
    address = models.CharField(_("Full Address"), max_length=500, default='', blank=False, null=True)
    city = models.CharField(_("City"), max_length=500, default='', blank=False, null=True)
    state = models.CharField(_("State"), max_length=500, default='', blank=False, null=True)
    zip_code = models.PositiveIntegerField(_("Zip Code"))
    items = models.CharField(_("Items"), max_length=10000, default='[]', blank=False, null=True)
    razp_amount = models.PositiveIntegerField(_("RazorPay Amount (in Rs.)"), null=True)
    razp_order_id = models.CharField(_("RazorPay Order ID"), max_length=100, default='', blank=False, null=True)
    razp_payment_id = models.CharField(_("RazorPay Payment ID"), max_length=100, default='', blank=False, null=True)
    razp_signature = models.CharField(_("RazorPay Signature"), max_length=100, default='', blank=False, null=True)
    status = models.CharField(_("Status"), max_length=50, choices=STATUS_CHOICES, default='pending')
    datetime = models.DateTimeField(_("Date & Time"), auto_now=True)

    def __str__(self) -> str:
        return 'Order ' + str(self.id) + ' - ' + self.user.username
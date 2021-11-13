from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import TextField

from django.utils.translation import ugettext_lazy as _

# Signal to create a user profile when a user is created
from django.dispatch import receiver
from django.db.models.signals import post_save

from shop.models import Product

# Create your models here.

gender_choices = (
    ('female', 'Female'),
    ('male', 'Male'),
    ('lgbtqia', 'LGBTQIA'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("Related User"), on_delete=models.CASCADE, related_name='userprofile')
    dob = models.DateField(_("Date of Birth"), blank=True, null=True)
    phone_no = models.IntegerField(_("Phone Number"), null=True)
    gender = models.CharField(_("Gender"), choices=gender_choices, max_length=7, blank=True)
    address = models.JSONField(_("Address"), default=dict, blank=True, null=True, encoder=None, decoder=None)
    cart = models.CharField(_("Cart"), max_length=10000, default='[]', blank=True, null=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return self.user.username
    
    def total_price(self):
        import json
        from django.shortcuts import get_object_or_404
        from shop.models import Product

        cart = json.loads(self.cart)

        total_price = 0
        for product in cart:
            product_net_price_each = get_object_or_404(Product, slug=product['slug']).net_price_each()
            total_price += product_net_price_each * product['quantity']
        
        return round(total_price, 2)
    
    # === PS: Ignore should have 'self' as first argument warning ===
    # Create a user profile when a user is created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
        
    # Create a user profile when a user is saved
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.user_profile.save()
    
    def get_full_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    
    def get_age(self):
        if self.dob:
            today = self.date.today()
            return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        else:
            return None

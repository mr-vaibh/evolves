from django.db import models

from django.utils.translation import ugettext_lazy as _

# Create your models here.

class FeaturedProduct(models.Model):
    product = models.ForeignKey("shop.Product", verbose_name=_("Related Product"), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'ID: {self.product.id}, ({self.product.name})'
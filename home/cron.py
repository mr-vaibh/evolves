from django.core.checks import messages
from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 0.01 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.cron.MyCronJob'    # a unique code

    def do(self):
        from home.models import FeaturedProduct
        from shop.models import Product, ProductReview

        from django.db.models import Avg

        for product in Product.objects.all():
            response = ProductReview.objects.filter(product=product).aggregate(Avg('stars'))

            if response['stars__avg'] > 4.2:
                FeaturedProduct.objects.update_or_create(product=product)
            else:
                messages = {
                    product.id: 'rating criteria didn\'t satisfied!' 
                }
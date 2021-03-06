# Generated by Django 3.2.8 on 2021-10-16 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image1',
            field=models.ImageField(null=True, upload_to='product_images/<built-in function id>/', verbose_name='Image 1'),
        ),
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(null=True, upload_to='product_images/<built-in function id>/', verbose_name='Image 2'),
        ),
        migrations.AddField(
            model_name='product',
            name='image3',
            field=models.ImageField(null=True, upload_to='product_images/<built-in function id>/', verbose_name='Image 3'),
        ),
        migrations.AddField(
            model_name='product',
            name='image4',
            field=models.ImageField(null=True, upload_to='product_images/<built-in function id>/', verbose_name='Image 4'),
        ),
        migrations.AddField(
            model_name='product',
            name='image5',
            field=models.ImageField(null=True, upload_to='product_images/<built-in function id>/', verbose_name='Image 5'),
        ),
        migrations.AddField(
            model_name='product',
            name='image6',
            field=models.ImageField(null=True, upload_to='product_images/<built-in function id>/', verbose_name='Image 6'),
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]

# Generated by Django 3.2.8 on 2021-10-12 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_userprofile_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(blank=True, verbose_name='Date of Birth'),
        ),
    ]

# Generated by Django 3.2.8 on 2021-10-15 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20211013_0723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_no',
            field=models.IntegerField(null=True, verbose_name='Phone Number'),
        ),
    ]

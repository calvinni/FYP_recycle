# Generated by Django 4.2.2 on 2023-08-15 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycle_app', '0008_available_vouchers_reedemed_vouchers_delete_vouchers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='available_vouchers',
            name='Discount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='reedemed_vouchers',
            name='Discount',
            field=models.IntegerField(),
        ),
    ]

# Generated by Django 4.2.2 on 2023-07-11 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recycle_app', '0003_bins'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appoinments',
            old_name='Status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='bins',
            old_name='Status',
            new_name='bin_location',
        ),
        migrations.AddField(
            model_name='bins',
            name='status',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]

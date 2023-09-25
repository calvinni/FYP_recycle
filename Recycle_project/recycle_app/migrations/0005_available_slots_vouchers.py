# Generated by Django 4.2.2 on 2023-08-06 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recycle_app', '0004_rename_status_appoinments_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Available_Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField(max_length=255)),
                ('available_timeslots', models.TimeField(max_length=255)),
                ('Availabilty', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vouchers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(max_length=255)),
                ('Code', models.CharField(max_length=255)),
                ('Usability', models.BooleanField(default=True)),
                ('exp_date', models.DateField(max_length=255)),
                ('user_id', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='recycle_app.users')),
            ],
        ),
    ]
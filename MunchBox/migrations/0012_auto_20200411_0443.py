# Generated by Django 3.0.3 on 2020-04-11 01:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MunchBox', '0011_auto_20200411_0054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='request_date',
        ),
        migrations.AddField(
            model_name='order',
            name='order_datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date and time of order'),
            preserve_default=False,
        ),
    ]
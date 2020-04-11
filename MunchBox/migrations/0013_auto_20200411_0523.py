# Generated by Django 3.0.3 on 2020-04-11 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MunchBox', '0012_auto_20200411_0443'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='request_productQty',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='request',
            unique_together={('request_orderID', 'request_productID')},
        ),
        migrations.RemoveField(
            model_name='request',
            name='request_customerID',
        ),
    ]

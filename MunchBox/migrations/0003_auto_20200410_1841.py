# Generated by Django 3.0.3 on 2020-04-10 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MunchBox', '0002_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_name', models.CharField(max_length=30, verbose_name='Product Name')),
                ('prod_cat', models.CharField(max_length=30, verbose_name='Product Category')),
                ('prod_qty', models.IntegerField(default=0, verbose_name='Product Quantity')),
                ('prod_price', models.DecimalField(decimal_places=5, max_digits=5, verbose_name='Product Price')),
                ('prod_bestSeller', models.CharField(max_length=30, verbose_name='Product Best Seller')),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_location',
            field=models.CharField(max_length=50, verbose_name='Customer Location'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='cust_name',
            field=models.CharField(max_length=30, verbose_name='Customer Name'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='supp_name',
            field=models.CharField(max_length=30, verbose_name='Supplier Name'),
        ),
    ]
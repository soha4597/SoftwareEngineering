from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Supplier, Product, Supply, Order, Request

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Supply)
admin.site.register(Order)
admin.site.register(Request)
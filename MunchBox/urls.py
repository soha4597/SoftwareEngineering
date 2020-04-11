from django.conf.urls import url
#from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$',views.index),
    url(r'add_customer',views.add_customer),
    url(r'add_supplier',views.add_supplier),
    url(r'add_product',views.add_product),
    url(r'supply_product',views.supply_product),
    url(r'add_request',views.add_request),
    url(r'add_order',views.add_order),
    url(r'index',views.index),
]

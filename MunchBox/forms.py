from django.forms import ModelForm
from .models import Customer,Supplier,Product,Supply,Order,Request
from django import forms
from django.utils.safestring import mark_safe

# Create the customer form class.
class CreateCustomerForm(ModelForm):
	class Meta:
		model = Customer
		#fields = "__all__"
		fields = ['cust_name', 'cust_location']

# Create the supplier form class.
class CreateSupplierForm(ModelForm):
	class Meta:
		model = Supplier
		fields = "__all__"
		#fields = ['supp_name']

# Create the product form class.
class CreateProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ['prod_name','prod_cat','prod_price']

# Create the supply form class.
class CreateSupplyForm(ModelForm):
	class Meta:
		model = Supply
		fields = "__all__"

class CreateOrderForm(ModelForm):
	class Meta:
		model = Order
		fields = ["order_customerID"]

# Create the request form class.
class CreateRequestForm(ModelForm):
	class Meta:
		model = Request
		fields = ["request_productID","request_productQty"]

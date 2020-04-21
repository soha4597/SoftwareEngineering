from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

# Create your models here.
#class Customer(models.Model):
 #   cust_name = models.CharField(verbose_name="Customer Name", max_length=30)
  #  cust_location = models.CharField(verbose_name="Customer Location",max_length=50)

   # def get_id(self):
    #    return self.id

class Supplier(models.Model):
    supp_name = models.CharField(verbose_name="Supplier Name", max_length=30)

    def get_id(self):
        return self.id

class Product(models.Model):
    prod_name = models.CharField(verbose_name="Product Name", max_length=30)
    prod_cat = models.CharField(verbose_name="Product Category",max_length=30)
    prod_qty = models.IntegerField(verbose_name="Product Quantity",default=0)
    prod_price = models.IntegerField(verbose_name="Product Price (in LL)")
    prod_bestSeller = models.CharField(verbose_name="Product Best Seller",max_length=30,default="Unknown Yet")

    suppliers = models.ManyToManyField(Supplier, through='Supply',through_fields=('supply_productID','supply_supplierID'))

    def get_id(self):
        return self.id

class Supply(models.Model):
    supply_supplierID = models.ForeignKey(Supplier,on_delete=models.CASCADE,verbose_name="Supplier ID")
    supply_productID = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product ID")
    supply_date = models.DateField(verbose_name="Date of supply")
    supply_qty = models.IntegerField(verbose_name="Quantity",validators=[MinValueValidator(1)])
    supply_cost = models.IntegerField(verbose_name="Cost of 1 item (in LL)",validators=[MinValueValidator(1)])

class Order(models.Model):
    order_customerID = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name="Customer ID",default=None, related_name = 'order')
    # When we build relations with the user model, this is what we use.
    order_totalPrice = models.IntegerField(verbose_name="Total Price",default=0)
    order_deliveryFee = models.IntegerField(verbose_name="Delivery Fee",validators=[MinValueValidator(1)],default=1)
    order_datetime = models.DateTimeField(auto_now_add=True,blank=True,verbose_name="Date and time of order")

    def get_id(self):
        return self.id

class Request(models.Model):
    request_orderID = models.ForeignKey(Order,on_delete=models.CASCADE,verbose_name="Order ID")
    request_productID = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Product ID")
    request_productQty = models.IntegerField(verbose_name="Quantity Requested",validators=[MinValueValidator(1)],default=1)
    request_profit = models.IntegerField(verbose_name="Profit",default=0)

    class Meta:
        unique_together = [['request_orderID','request_productID']]

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .forms import CreateCustomerForm,CreateSupplierForm,CreateProductForm,CreateSupplyForm,CreateOrderForm,CreateRequestForm
from .models import Customer,Supplier,Product,Supply,Order,Request

# Create your views here.



def index(request):
    #[Supply.objects.filter(id=(i+1)).delete() for i in range(20)]
    #[Product.objects.filter(id=(i + 1)).delete() for i in range(20)]
    #[Supplier.objects.filter(id=(i + 1)).delete() for i in range(20)]
    #[Order.objects.filter(id=(i + 1)).delete() for i in range(20)]
    #[Request.objects.filter(id=(i+1)).delete() for i in range(20)]

    return render(request, 'index.html')

def add_customer(request):
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            customerform = form.cleaned_data
            cust_name = customerform['cust_name']
            cust_location = customerform['cust_location']
            Customer.objects.create(cust_name=cust_name, cust_location=cust_location)
            return render(request, 'index.html')
    else:
        form = CreateCustomerForm()
    S = Customer.objects.all()
    return render(request, 'add_customer.html', {'form': form, 'S': S})

def add_supplier(request):
    if request.method == 'POST':
        form = CreateSupplierForm(request.POST)
        if form.is_valid():
            supplierform = form.cleaned_data
            supp_name = supplierform['supp_name']
            Supplier.objects.create(supp_name=supp_name)
            return render(request, 'index.html')
    else:
        form = CreateSupplierForm()
    S = Supplier.objects.all()
    return render(request, 'add_supplier.html', {'form': form, 'S': S})

def add_product(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST)
        if form.is_valid():
            productform = form.cleaned_data
            prod_name = productform['prod_name']
            prod_cat = productform['prod_cat']
            prod_price = productform['prod_price']
            Product.objects.create(prod_name=prod_name,prod_cat=prod_cat,prod_price=prod_price)
            return render(request, 'index.html')
    else:
        form = CreateProductForm()
    S = Product.objects.all()
    return render(request, 'add_product.html', {'form': form, 'S': S})

def supply_product(request):
    if request.method == 'POST':
        form = CreateSupplyForm(request.POST)
        if form.is_valid():
            supplyform = form.cleaned_data
            supply_supplierID = supplyform['supply_supplierID']
            supply_productID = supplyform['supply_productID']
            supply_date = supplyform['supply_date']
            supply_qty = supplyform['supply_qty']
            supply_cost = supplyform['supply_cost']

            Supply.objects.create(supply_supplierID=supply_supplierID,supply_productID=supply_productID,
                                  supply_date=supply_date,supply_qty=supply_qty,supply_cost=supply_cost)

            pID = supply_productID.get_id()
            product = Product.objects.get(id=pID)
            product.prod_qty += supply_qty
            product.save()

            return render(request, 'index.html')
    else:
        form = CreateSupplyForm()
    S = Supply.objects.all()
    return render(request, 'supply_product.html', {'form': form, 'S': S})

def add_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            orderform = form.cleaned_data
            order_customerID = orderform['order_customerID']

            order = Order.objects.create(order_customerID=order_customerID)
            request.session['selected_orderID'] = order

            form = CreateRequestForm()
            S = Request.objects.all()
            return render(request, 'add_request.html', {'form': form, 'S': S})
    else:
        form = CreateOrderForm()
    S = Order.objects.all()
    return render(request, 'add_order.html', {'form': form, 'S': S})

def add_request(request):
    print(request.method)
    if request.method == 'POST':
        form = CreateRequestForm(request.POST)
        if form.is_valid():
            requestform = form.cleaned_data
            request_productID = requestform['request_productID']
            request_productQty = requestform['request_productQty']
            print("Reached here 3")
            request_orderID = Order(request.session['selected_orderID'])
            print("Reached here 4")
            Request.objects.create(request_productID=request_productID,
                                   request_productQty=request_productQty,
                                   request_orderID=request_orderID)
            return render(request, 'index.html')
    else:
        form = CreateRequestForm()
    S = Request.objects.all()
    return render(request, 'add_request.html', {'form': form, 'S': S})

from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404


from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm,CreateSupplierForm, EditCustomer,CreateProductForm
from .filters import OrderFilter
from .decorators import *

from django.contrib.auth.models import User
from django.contrib import messages 


@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)

			Customer.objects.create(
				cust_user=user,
				cust_name=user.username,
                cust_email=user.email,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def editProfile(request):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, cust_email= request.user.customer.cust_email)
        bound_form = EditCustomer(request.POST, instance = customer)
        if bound_form.is_valid():
            new_customer = bound_form.save()
            request.user.username = new_customer.cust_name
            request.user.email = new_customer.cust_email
            return redirect('user-page')
        else:
            context = { 'form': bound_form }
            return render(request, 'accounts/editProfile.html', context)
    else:
        customer = get_object_or_404(Customer, cust_email= request.user.customer.cust_email)
        bound_form = EditCustomer(request.POST, instance=customer)
        context = {'form': bound_form}
        return render(request, 'accounts/editProfile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def viewProfile(request):
    customer = get_object_or_404(Customer, cust_email= request.user.customer.cust_email)
    id = request.user.pk
    context = { 'customer': customer, "id": id }
    return render(request, 'accounts/viewProfile.html', context)


@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(order_status='Delivered').count()
	pending = orders.filter(order_status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(order_status='Delivered').count()
    pending = orders.filter(order_status='Pending').count()

    context = {'orders':orders,'total_orders':total_orders,
    'delivered':delivered,'pending':pending,}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def suppliers(request):
    suppliers = Supplier.objects.all()
    return render(request,'accounts/suppliers.html',{'suppliers':suppliers})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createSupplier(request):
    if request.method == 'POST':
        form = CreateSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CreateSupplierForm()
    context = {'form':form}
    return render(request,'accounts/create_supplier.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    
    orders = customer.order_set.all()
    orders_count = orders.count()

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs

    total_orders = orders.count()
    delivered = orders.filter(order_status='Delivered').count()
    pending = orders.filter(order_status='Pending').count()

    context = {'orders':orders,'total_orders':total_orders,
    'delivered':delivered,'pending':pending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def createOrder(request):
    if( request.user.customer.cust_location == None or request.user.customer.cust_location == None):
        return render(request, "accounts/valid_info.html")
    
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('order_product','order_quantity'),extra=5)
    #customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none())#,instance=customer)
    #form = OrderForm(initial={'order_customer':customer})
    if request.method=="POST":
        customer = Customer.objects.get(cust_user=User(id=request.user.id))
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    products = Product.objects.all()
    context={'formset':formset,'products':products}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method=="POST":
        #print("Printing post:",request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'accounts/update_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)

    if request.method=="POST":
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request,'accounts/delete.html',context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):
    if request.method=="POST":
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            prodform = form.cleaned_data
            Name = prodform['prod_name']
            Category = prodform['prod_cat']
            Quantity = prodform['prod_qty']
            Price = prodform['prod_price']
            Bestseller = prodform['prod_bestSeller']
            image = prodform['prod_img']
            Product.objects.create(prod_name=Name, prod_cat = Category, prod_qty = Quantity, prod_price= Price, prod_bestSeller = Bestseller, prod_img = image)
            products = Product.objects.all()
            return render(request, 'accounts/products.html', {'products': products})
    else:
        form = CreateProductForm()
    return render(request,'accounts/create_product.html', {'form':form})

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



from .models import Order,Supplier,Customer,Product


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class CreateSupplierForm(ModelForm):
	class Meta:
		model = Supplier
		fields = ['supp_name','supp_phone','supp_email']

class EditCustomer(ModelForm):
	class Meta:
		model = Customer
		fields = ['cust_name', 'cust_location', 'cust_phone', 'cust_email' ]
        
class CreateProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ['prod_name','prod_cat','prod_qty','prod_price','prod_bestSeller', 'prod_img']
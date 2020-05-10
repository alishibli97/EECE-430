from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    cust_user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    cust_name = models.CharField(verbose_name="Customer Name", max_length=30, null=True)
    cust_location = models.CharField(verbose_name="Customer Location",max_length=50, null=True)
    cust_phone = models.CharField(verbose_name="Customer Phone Number",max_length=20, null=True)
    cust_date_created = models.DateTimeField(auto_now_add=True, null=True)
    cust_email = models.CharField(verbose_name="Customer Email",max_length=30,unique=True)


    def __str__(self):
        return self.cust_name

class Tag(models.Model):
    tag_name = models.CharField(verbose_name="Tag Name", max_length=30, null=True)

    def __str__(self):
        return self.tag_name

class Product(models.Model):
    CATEGORY = (
        ('Baked Goods','Baked Goods'),
        ('Bread','Bread'),
        ('Breakfast', 'Breakfast'),
        ('Candy', 'Candy'),
        ('Care Products', 'Care Products'),
        ('Chips', 'Chips'),
        ('Chocolate', 'Chocolate'),
        ('Cookies', 'Cookies'),
        ('Dairy', 'Dairy'),
        ('Drinks', 'Drinks'),
        ('Dry Goods', 'Dry Goods'),
        ('Healthy Snacks', 'Healthy Snacks'),
        ('Ice Cream', 'Ice Cream'),
        ('Spreads', 'Spreads'),
    )
    
    prod_name = models.CharField(verbose_name="Product Name", max_length=30,null=True)
    prod_cat = models.CharField(verbose_name="Product Category",max_length=30,null=True,choices=CATEGORY)
    prod_qty = models.IntegerField(verbose_name="Product Quantity",default=0,null=True)
    prod_price = models.FloatField(verbose_name="Product Price (in LL)",null=True)
    prod_bestSeller = models.CharField(verbose_name="Product Best Seller",max_length=30,default="Unknown Yet",null=True)
    prod_dateAdded = models.DateTimeField(auto_now_add=True,null=True)
    prod_img = models.ImageField(default='logo.PNG', blank = True, null = True)
    #tags = models.ManyToManyField(Tag,null=True,blank=True)

    def _str_(self):
        return self.prod_name
        
class Order(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered')
    )

    order_customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, verbose_name="Customer",null=True)
    order_product = models.ForeignKey(Product,on_delete=models.SET_NULL,verbose_name="Product",null=True)
    # When we build relations with the user model, this is what we use.
    order_totalPrice = models.IntegerField(verbose_name="Total Price",default=0)
    order_deliveryFee = models.IntegerField(verbose_name="Delivery Fee",validators=[MinValueValidator(1)],default=1)
    order_datetime = models.DateTimeField(auto_now_add=True,blank=True,verbose_name="Date and time of order")
    order_status = models.CharField(max_length=50,null=True,choices=STATUS,default="Pending")
    order_note = models.CharField(verbose_name="Note",max_length=100,null=True)
    order_quantity = models.IntegerField(verbose_name="Quantity",validators=[MinValueValidator(1)],default=0)

    def __str__(self):
        return self.order_product.prod_name

class Supplier(models.Model):
    supp_user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    supp_name = models.CharField(verbose_name="Supplier Name", max_length=30, null=True)
    supp_phone = models.CharField(verbose_name="Supplier Phone Number",max_length=20, null=True)
    supp_email = models.CharField(verbose_name="Supplier Email",max_length=30,null=True)
    supp_date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.supp_name

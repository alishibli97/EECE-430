from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('editProfile/' , views.editProfile, name ='edit'),
    path('viewProfile/' , views.viewProfile, name ='view'),

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('products/', views.products, name='products'),
    path('suppliers/', views.suppliers, name='suppliers'),
    path('create_supplier/', views.createSupplier, name="create_supplier"),
    path('customer/<str:pk>/', views.customer, name="customer"),

    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    
    path('create_product/', views.createProduct, name="create_product"),

]

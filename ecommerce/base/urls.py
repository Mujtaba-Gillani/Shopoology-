from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='home')  ,  
    path('store/', views.Store, name='store'),    
    path('cart/', views.Cart, name='cart'),    
    path('checkout/', views.Checkout, name='checkout'),    
    path('update_item/', views.updateItem, name='update_item'),    
    path('process_order/', views.processOrder, name='product_order'),   
    path('login/',views.Login_view, name='login'),
    path('signup/',views.SignUp_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

]
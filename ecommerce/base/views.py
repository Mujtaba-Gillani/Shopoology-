from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .models import *
import uuid
import json
import datetime
from .utils import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required


# Create your views here.

#home function
def Home(request):
    if request.user.is_authenticated:
        try:
            user_profile = request.user.user_profile
            customer = get_object_or_404(UserProfile, user=request.user)
            order, created = Order.objects.get_or_create(user=customer.user, complete=False)

            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        except UserProfile.DoesNotExist:
            user_profile = None
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = order['get_cart_items']
        
    else:
        items=[]
        order={'get_cart_total':0, 'get_cart_items':0}
        cartItems=order['get_cart_items']
        
    context={'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, 'base/home.html', context)

#cart function
def Cart(request):
    data=cartData(request)
    items=data['items']
    order=data['order']
    cartItems=data['cartItems']
    context={'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'base/cart.html', context)

#store function
def Store(request):
    data=cartData(request)
    cartItems=data['cartItems']
    
    
    product=Product.objects.all()
    
    context={'products':product, 'cartItems':cartItems}
    return render(request, 'base/store.html', context)

#checkout function

def Checkout(request):

    data=cartData(request)
    cartItems=data['cartItems']
    items=data['items']
    order=data['order']
    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'base/checkout.html', context)


def updateItem(request):
    data= json.loads(request.body)
    productId= data['productId']
    action = data['action']
    # print('Action: ', action)
    # print('Product: ', productId)
    customer=request.user.customer
    product= Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':    
        orderItem.quantity = (orderItem.quantity -1)
    orderItem.save()
    
        
    if orderItem.quantity<=0:
        orderItem.delete()
        
    order_items=order.orderitem_set.all()
    items=[{
        'product':{
            'id':item.product.id,
            'name':item.product.name,
            'price':item.product.price,
            'imageURL':item.product.imageURL
        },
        'quantity':item.quantity,
        'get_total':item.get_total,
    } 
        for item in order_items]
    cart_info={
            'get_cart_total':order.get_cart_total,
            'get_cart_items':order.get_cart_items,
            'shipping':order.shipping,
        }
    response_data={'items':items, 'order':cart_info}
    return JsonResponse(response_data, safe=False)

@csrf_exempt
def processOrder(request):
    # transaction_id = str(uuid.uuid4())
    transaction_id=datetime.datetime.now().timestamp()
    data= json.loads(request.body)
    
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)


    else:
        customer, order=guestOrder(request, data)
        
    total=float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
        order.complete=True
    order.save()
    
    if order.shipping== True:
        Shipping_Address.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            country=data['shipping']['country'],
            contact=data['shipping']['contact'],
    )
    return JsonResponse('Payment Done', safe=False)



def Login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username, password=password)
        
        if user is not  None:
            login(request, user)
            return redirect('home')
        
    return render(request,'base/login.html')

def SignUp_view(request):
    context = {}

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            user_profile = UserProfile.objects.create(user=user)
            user_profile.full_name = form.cleaned_data['fullname']
            user_profile.email = form.cleaned_data['email']
            user_profile.phone_number = int(form.cleaned_data['phone_number'])
            user_profile.user_type = form.cleaned_data['user_type']
            user_profile.gender = form.cleaned_data['gender']
            user_profile.date_of_birth = form.cleaned_data['date_of_birth']
            user_profile.save()

            user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            login(request, user)

            return redirect('home')
        else:
            context = {'form': form}
    else:
        form = SignUpForm()
        context = {'form': form}

    return render(request, 'base/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')
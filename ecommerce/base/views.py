from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import uuid
import json
import datetime
from .utils import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#home function
def Home(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order, created= Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
        
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


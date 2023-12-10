from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import *
from order import models as ordermodels
from home import views as homeviews
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import date
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def cart(request):
    return render(request, 'cart.html')


@login_required
def view_cart(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cartItems = CartItem.objects.filter(cart=cart) 
    totalPrice = sum(item.game.price * item.quantity for item in cartItems)
    
    shippingPrice = 10
    cartIsEmpty = False
    #Check if cart is empty
    if(cartItems.count() < 1):
        cartIsEmpty = True
        shippingPrice = 0
    return render(request, 'cart.html', {'user':request.user, 'cart_items': cartItems, 'total_price': totalPrice, 'cart_is_empty': cartIsEmpty, 'shipping_price': shippingPrice})

def remove_from_cart(request, cartItemId):
    #Remove from Cart
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cartItems = CartItem.objects.filter(cart=cart, pk=cartItemId)
    cartItems.delete()

    return redirect(view_cart)


def GetNumberOfCartItem(request):
    print("Get number in cart is running")
    if request.method == 'GET':
        cart = ordermodels.Cart.objects.get_or_create(user=request.user)[0]
        itemInCart = ordermodels.CartItem.objects.filter(cart = cart).count()
        return JsonResponse({"Success": True, "itemInCart": itemInCart})


@csrf_exempt
def UpdateCartItemQuantity(request):
    if request.method =='PATCH':
        print("Update cart item quantity")
        # Assuming the data sent in the request is in JSON format
        jsonData = json.loads(request.body.decode('utf-8'))
    
        #userId = jsonData['data']['userId']
        operation =jsonData['data']['operation']
        cartItemId =jsonData['data']['cartItemId']

        print(f"operation: {operation}")
        print(f"cart item id: {cartItemId}")
        #Get the cart item and increase the count
        cartItem = ordermodels.CartItem.objects.get(pk=cartItemId) 

        if operation == "increment":
            cartItem.quantity += 1
        elif operation == "decrement":
            cartItem.quantity -=1
        else:
            pass
        
        cartItem.save()

        #Update order total
        cart = Cart.objects.get_or_create(user=request.user)[0]
        cartItems = CartItem.objects.filter(cart=cart) 
        totalPrice = sum(item.game.price * item.quantity for item in cartItems)

        return JsonResponse({"Success": True, "newQuantity": cartItem.quantity, 'newTotal': totalPrice})


def convert_cart_to_order(request):
    if request.method == "POST":
        print("Converting cart to order")
        
        
        user = request.user
        print(user)
        ucart = Cart.objects.get(user=user)
        print(ucart)

        cart_items = CartItem.objects.filter(cart=ucart)
        print(cart_items)

        #
        uorder = Order.objects.create(user=user, totalPrice= 1.0, orderDate=date.today(), isShipped=False, isReceived=False)
        print(uorder)

        cart_items = CartItem.objects.filter(cart=ucart)
        print(cart_items)

        for cart_item in cart_items:
            #If the edition is physical, minus off from the physical stock count
            if cart_item.edition == "physical":
                game = browsemodels.Game.objects.get(pk = cart_item.game.id)
                game.physicalCopyQuantity = game.physicalCopyQuantity - cart_item.quantity
                game.save()
        
            OrderItem.objects.create(
                order= uorder,
                game = cart_item.game.name,
                edition = cart_item.edition,
                platform = cart_item.platform,
                quantity = cart_item.quantity,
                price = cart_item.game.price
            )

            
        order_items = OrderItem.objects.filter(order = uorder)    

        uorder.totalPrice = sum(item.price * item.quantity for item in order_items)
        uorder.orderDate = date.today()
        uorder.isShipped = False
        uorder.isReceived = False
        uorder.save()

        # Delete the original cart and cart items
        cart = Cart.objects.get(user=user)
        cart.delete()
        return redirect(homeviews.home)
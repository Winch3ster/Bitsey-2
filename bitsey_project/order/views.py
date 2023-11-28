from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import *
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
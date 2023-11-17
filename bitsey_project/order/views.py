from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

def cart(request):
    return render(request, 'cart.html')


#@login_required
def view_cart(request):
    cart = Cart.objects.get_or_create(user=request.user)[0]
    cartItems = CartItem.objects.filter(cart=cart) 
    totalPrice = sum(item.product.price * item.quantity for item in cartItems)
    
    return render(request, 'cart/view_cart.html', {'cart_items': cartItems, 'total_price': totalPrice})
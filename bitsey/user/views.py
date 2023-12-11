from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponse
from .userForms import *
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate
from home import views as homeviews
from order import models as ordermodels
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
import json


# Create your views here.
def signin(request):
    if request.method == 'POST':
        print("This sign in POST is running")
        signIn_form = userSignInForm(request.POST)
        if signIn_form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            #user = User.objects.get(username = username, password=password)
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            print("This is user" + str(user))
            if user is not None:
                
                login(request, user)
                homeURL = reverse('homepage')
                return redirect(homeURL)
            else:
                return render(request, 'signin.html', {'signIn_form': signIn_form, 'errorMessage': "Incorrect username or password"})
    
        else:
            print("User form is invalid")
            print(signIn_form.errors)  # Add this line to print form errors
            return render(request, 'signin.html', {'signIn_form': signIn_form, 'errorMessage': "Please enter valid credentials"})
    
    else:
        print("This is working from sign in Hello World")
        signIn_form = userSignInForm()
        return render(request, 'signin.html', {'signIn_form': signIn_form})




def signup(request):
    # If the user send POST request 
    if request.method == 'POST':
        print("Sign up post is running")
        #Create new form and filled it with data from POST request
        user_form = userForm(request.POST, prefix='user')
        address_form = addressForm(request.POST, prefix='address')
        #combined_form = CombinedForm(request.POST, instance=User(), prefix='combined')

        #Check if form is valid 
        if user_form.is_valid() and address_form.is_valid():
            print("Form is valid")
            fname = user_form.cleaned_data["firstName"]
            lname = user_form.cleaned_data["lastName"]
            uname = user_form.cleaned_data["username"]
            email = user_form.cleaned_data["email"]
            pw = user_form.cleaned_data["password"]
            #'firstName','lastName','username', 'email', 'password'
            new_user = User.objects.create(firstName=fname, lastName=lname, username=uname, email=email, password=pw)
            new_user.set_password(pw)
            new_user.save()

            #user = user_form.save(commit=False)
            #['streetLine1', 'streetLine2', 'city', 'state', 'postalCode', 'country']
            address = address_form.save(commit=False)
            streetL1 = address_form.cleaned_data["streetLine1"]
            streetL2 = address_form.cleaned_data["streetLine2"]
            city = address_form.cleaned_data["city"]
            state = address_form.cleaned_data["state"]
            postalcode = address_form.cleaned_data["postalCode"]
            country = address_form.cleaned_data["country"]

            new_user_address = Address(user=new_user, streetLine1 = streetL1, streetLine2 = streetL2, city = city, state = state, postalCode = postalcode, country = country)
            new_user_address.save()
            print(address)

            address.user = new_user
            print(address.user.username)
            address.save()
            #login(request, new_user)

            return redirect(signin)

    else:
        #When user first entered the page it will be GET so this will run

        #Create empty form with prefixes
        user_form = userForm(prefix='user')
        address_form = addressForm(prefix='address')

        #combined_form = CombinedForm(instance=User(), prefix='combined')

    return render(request, 'register.html', {
        'user_form': user_form,
        'address_form': address_form,
    })

   





def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_address = get_object_or_404(Address, user__id=user_id)

    if request.method == 'POST':

        filled_user_form = userForm(request.POST, instance=user, prefix='user')
        filled_address_form = addressForm(request.POST, instance=user_address, prefix='address')
         
        if filled_user_form.is_valid() and filled_address_form.is_valid():
            filled_user_form.save()
            filled_address_form.save()
            return HttpResponse("Successfully edited user")
    else:
        form = userForm(instance=user, prefix='user')
        address_form =  addressForm (instance=user_address, prefix='address')
         
    return render(request, 'account.html', {'form': form,'address_form': address_form,'user': user})






def userDataViewer(request):
    users = User.objects.all()
    return render(request, 'dataviewer.html', {'users': users})


@csrf_exempt
def WishListItemCreate(request):
    if request.method == 'POST':
        # Assuming the data sent in the request is in JSON format
        jsonData = json.loads(request.body.decode('utf-8'))
    
        #userId = jsonData['data']['userId']
        gameId =jsonData['data']['gameId']

        #get the games and user
        #user = User.objects.get(pk=userId)
        game = browsemodels.Game.objects.get(pk=gameId)

        wishList, wishListCreated = UserWishList.objects.get_or_create(user=request.user)

        wishListItem, wishListItemCreated = WishListItem.objects.get_or_create(wishList= wishList, game = game)

        if not wishListItemCreated:
            #if game already in wishlist, remove it
            wishListItem.delete()
            return JsonResponse({"status": "RemovedItem"})
        
        return JsonResponse({"status": "Success"})
    
    #If it is not a post request, assume it is a GET request for all user's wishlist items
    else:
        wishList, wishListCreated = UserWishList.objects.get_or_create(user=request.user)
        wishListItems = WishListItem.objects.filter(wishList = wishList)

        wishListItemsId = []
        for item in wishListItems:
            wishListItemsId.append(item.game.id)
       
        return JsonResponse({"userWishListItems": wishListItemsId})


@login_required
def view_wishlist(request):
    print("view wishlist is running")
    wishlist = UserWishList.objects.get_or_create(user=request.user)[0]
    print(request.user)
    print(wishlist)
    wishlistItems = WishListItem.objects.filter(wishList = wishlist)

    
    return render(request, 'wishlist.html', {'wishlistItems': wishlistItems })

def remove_from_wishList(request, wishListItemId):
    #Remove from wishlist

    uwishlist = UserWishList.objects.get_or_create(user=request.user)[0]
    wishListItem = WishListItem.objects.filter(wishList =uwishlist, pk=wishListItemId)
    wishListItem.delete()

    return redirect(view_wishlist)

def view_purchase_history(request):
    print("view_purchase_history")
    user = request.user
    #Get all the order history
    orders = ordermodels.Order.objects.filter(user=user)
    order_items = ordermodels.OrderItem.objects.filter(order__in=orders)

    print("Order Items: " + str(order_items))
    noOrder = True
    if orders is not None:
        noOrder = False

    #Create JSON for it
    print("Order items: " + str(order_items))

    return render(request, 'purchasehistory.html', {'orders': orders,'order_items': order_items ,'noOrder':noOrder} )


def order_received(request, orderId):
    pass
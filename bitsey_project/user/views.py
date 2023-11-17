from django.shortcuts import render
from django.http import HttpResponse
from .userForms import *
from .models import *
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
def signin(request):
    if request.method == 'POST':
        signIn_form = userSignInForm(request.POST)

        if signIn_form.is_valid():
            credentials = signIn_form.save(commit=False)
            # perform validation
            print(credentials.username)
            print(credentials.password)
            
            if User.objects.filter(username= credentials.username, password=credentials.password).exists():
                return HttpResponse('Found user')
            else:
                
                return render(request, 'signin.html', {'signIn_form': signIn_form, 'errorMessage': "Incorrect username or password"})

            # check if user exist
            # if yes redirect to homepage
            # if no, display error
    else:    
        signIn_form = userSignInForm()

    return render(request, 'signin.html', {
        'signIn_form': signIn_form,
    })

    #return HttpResponse("Hello world! this is supposingly from sign in html")

#def signUp(request):
    #form = userForm()
    #return render(request, 'register.html', {'form': form})

#def signUpValidation(request)



def signup(request):
    # If the user send POST request 
    if request.method == 'POST':
        print("Post request received")
        #Create new form and filled it with data from POST request
        user_form = userForm(request.POST, prefix='user')
        address_form = addressForm(request.POST, prefix='address')
        #combined_form = CombinedForm(request.POST, instance=User(), prefix='combined')
        print(user_form.is_valid())
        print(address_form)
        print("Address form " + str(address_form.is_valid()))
        #Check if form is valid 
        if user_form.is_valid() and address_form.is_valid():
            print("form is valid")
            user = user_form.save()

            address = address_form.save(commit=False)
            address.user = user
            address.save()

            return HttpResponse("successfully saved user")

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

   
def cart(request):
    return render(request, 'cart.html')





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
    return render(request, 'account.html', {'form': form, 'address_form': address_form,'user': user})


def wishlist(request, user_id):
    # will return games and user
    return render(request, 'wishlist.html', {'form': form, 'address_form': address_form,'user': user})


def userDataViewer(request):
    users = User.objects.all()
    return render(request, 'dataviewer.html', {'users': users})

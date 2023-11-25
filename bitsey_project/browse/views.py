from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from .models import *
from order import models as ordermodels


# Create your views here.
def browse(request):
    returnedGames = Game.objects.all()
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'store.html', {'returnedGames': returnedGames, 'user': user})



    
    return render(request, 'store.html', {'returnedGames': returnedGames})
    #return HttpResponse("Hello world! this i supposingly from homepahe html")


def game_detail(request, game_id):
    returnedGame = Game.objects.get(pk=game_id)
    


    returnedGameplayImages = GameplayImage.objects.filter(game = returnedGame)
    print("This is the returned gameplayImages")
    print(returnedGameplayImages)
    return render(request, 'game.html', {'returnedGame': returnedGame,
                                         'returnedGameplayImages': returnedGameplayImages
                                         })



def addToCart(request, gameId):
    if request.method == 'POST':
        #check if user is logged in 
        #If YES, proceed 
        #If NO, redirect to front end

        if request.user.id != None:

            print(request.user.id)
            print("New")
            # Process form data
            userPickedEdition = request.POST.get('edition')
            userPickedplatform = request.POST.get('platform')

            game = get_object_or_404(Game, pk=gameId)

    
            cart, created = ordermodels.Cart.objects.get_or_create(user=request.user) #created will set to true if object can't befound an d a new is created
            


        
            cart_item, item_created = ordermodels.CartItem.objects.get_or_create(cart=cart, game=game, edition=userPickedEdition, platform=userPickedplatform)
        
            #This translate to if item is not created, which means it is already in the cart
            if not item_created:
                # If the product is already in the cart, increase the quantity
               cart_item.quantity += 1
               cart_item.save()
            
            return HttpResponse("Successfully added to cart")
        else:
            return redirect('signin')        


def get_game_platform_data(request, gameId):
    game= Game.objects.get(pk=gameId)
    validGamePlatform = []
    for x in game.platforms.all():
        validGamePlatform.append(x.platformName)
    data = {'gamePlatformArray': validGamePlatform}
    return JsonResponse(data)

def search_for_game(request):
    query = request.GET.get('search', '')
    results = Game.objects.filter(name__icontains=query)[:10]  # Adjust the field based on your model
    print("This is running")
    print(query)
    print(results)
    if results is not None:
        return render(request, 'store.html', {'returnedGames': results})
    else:
        return redirect(browse)
   

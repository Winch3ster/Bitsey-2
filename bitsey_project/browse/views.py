from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect


from .models import *
from order import models as ordermodels


# Create your views here.
def browse(request):
    returnedGames = Game.objects.all()
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
    game = get_object_or_404(Game, pk=gameId)
    cart, created = ordermodels.Cart.objects.get_or_create(user=request.user) #created will set to true if object can't befound an d a new is created
    
    # Check if the product is already in the cart
    cart_item, item_created = ordermodels.CartItem.objects.get_or_create(cart=cart, game=game)
    
    #This translate to if item is not created, which means it is already in the cart
    if not item_created:
        # If the product is already in the cart, increase the quantity
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')





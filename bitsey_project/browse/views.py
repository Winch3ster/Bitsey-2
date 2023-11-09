from django.shortcuts import render
from django.http import HttpResponse
from .models import *

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




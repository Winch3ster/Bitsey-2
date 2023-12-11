from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from .models import *
from order import models as ordermodels
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .serializer import GameSerializer
from django.utils import timezone
from django.shortcuts import redirect
from system import models as sysmodels
from user import views as uviews


# Create your views here.
def browse(request):
    returnedGames = Game.objects.all()
    NewRelease = Game.objects.all()
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'store.html', {'returnedGames': returnedGames, 'user': user, 'search': 'All', 'NewRelease': NewRelease})



    
    return render(request, 'store.html', {'returnedGames': returnedGames, 'search': 'All'})
    #return HttpResponse("Hello world! this i supposingly from homepahe html")


def game_detail(request, game_id):
    if request.method == 'POST':
         #check if user is logged in 
        #If YES, proceed 
        #If NO, redirect to front end
        if request.user.id != None:
            # set the trial date
            cGame = Game.objects.get(pk=game_id)
            trial = sysmodels.Trial(user=request.user, game = cGame, date = timezone.now(), approved= False)
            
            trial.save()
            returnedGame = Game.objects.get(pk=game_id)
            
            returnedGameplayImages = GameplayImage.objects.filter(game = returnedGame)
            print("This is the returned gameplayImages")
            print(returnedGameplayImages)
            return render(request, 'game.html', {'returnedGame': returnedGame,
                                                'returnedGameplayImages': returnedGameplayImages,
                                                'TrialRequested' : True
                                                })
        else:
              return redirect(uviews.signin)
    else:    

        returnedGame = Game.objects.get(pk=game_id)
        
        returnedGameplayImages = GameplayImage.objects.filter(game = returnedGame)
        print("This is the returned gameplayImages")
        print(returnedGameplayImages)
        return render(request, 'game.html', {'returnedGame': returnedGame,
                                            'returnedGameplayImages': returnedGameplayImages,
                                            'TrialRequested' : False
                                            })


def addToCart(request, gameId):
    if request.method == 'POST':
        #check if user is logged in 
        #If YES, proceed 
        #If NO, redirect to front end
        if request.user.id != None:

            print(request.user.id)
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
            
            itemInCart = ordermodels.CartItem.objects.filter(cart = cart).count()
            return JsonResponse({"Success": True, "itemInCart": itemInCart})
        else:
            return JsonResponse({"Success": False})
            return redirect(uviews.signin)    


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
   



#Searching and filtering code API
@csrf_exempt
def SearchFilter(request):
    print("Search filter is working This is one")
    if request.method == 'PATCH':
        print("Search filter is working this is after if")
        data = json.loads(request.body)
        #selected_platforms = data.get('queries', [])

        platform_to_search = data.get('queries').get('platform')
        
        genre_to_search = data.get('queries').get('genre')

        orderBy = data.get('queries').get('orderby')
        print(orderBy)

        if not platform_to_search and not genre_to_search:

            result = Game.objects.all()

            if len(orderBy) > 0:
                if orderBy[0] =='SortByIncreasingPrice':
                    sortedResult = sorted(result, key=lambda x: x.price)
                elif orderBy[0] == 'SortByDecresingPrice':
                    sortedResult = sorted(result, key=lambda x: x.price, reverse=True)
                else:
                    sortedResult = result
            else:
                sortedResult = result


            serializer = GameSerializer(sortedResult, many=True)
            json_data = serializer.data

            return JsonResponse({'result': json_data})
        else:
                
            print(platform_to_search)
        
            print(genre_to_search)

            platform_to_search_result = []
            genre_to_search_result =[]
            #Search game based on platforms first
            if len(platform_to_search) == 0:
                print(f"Platform to search is none: {platform_to_search}" )
            else:
                print(f"Search game based on platform from this: {platform_to_search}" )
                platform_to_search_result = Game.objects.filter(platforms__platformName__in=platform_to_search)
        
            #Search game based on genre

            if len(genre_to_search) == 0:
                print(f"Genre to search is none: {genre_to_search}" )
            else:
                genre_to_search_result  = Game.objects.filter(gameCategories__category__in=genre_to_search)
                print(f"Search game based on genre from this: {genre_to_search}" )

            #If the to be search is none, then skip
            #Combine all the platform and genre search results into a single unique list by using the intersection method
            print(f"Result on platform: {platform_to_search_result}")
            print(f"Result on genre: {genre_to_search_result}")

        
            # Check if either list is empty
            if not platform_to_search:
                result = list(set(genre_to_search_result))
            elif not genre_to_search:
                result = list(set(platform_to_search_result)) 
            else:
                # Find the common elements
                common_elements = set(platform_to_search_result).intersection(set(genre_to_search_result))
                result = list(common_elements)
            
            if len(orderBy) > 0:
                if orderBy[0] =='SortByIncreasingPrice':
                    sortedResult = sorted(result, key=lambda x: x.price)
                elif orderBy[0] == 'SortByDecresingPrice':
                    sortedResult = sorted(result, key=lambda x: x.price, reverse=True)
                else:
                    sortedResult = result
            else:
                sortedResult = result

            # Perform filtering based on selected platforms in  model/queryset

            # Convert queryset to a list of dictionaries
            #games_list = list(games)

            serializer = GameSerializer(sortedResult, many=True)
            json_data = serializer.data

            # Return filtered data as JSON response
            return JsonResponse({'result': json_data})

    return JsonResponse({'error': 'Invalid request method'})

def SearchFromHomeHorror(request):
    returnedGames = Game.objects.filter(gameCategories__category__icontains ='Horror' ) | Game.objects.filter(gameCategories__category__icontains ='Adventure' )
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'store.html', {'returnedGames': returnedGames, 'user': user, 'search': 'Horror'})
    return render(request, 'store.html', {'returnedGames': returnedGames, 'search': 'Horror'})


@csrf_exempt
def SearchFromHomeWar(request):
    returnedGames = Game.objects.filter(gameCategories__category__icontains ='War') | Game.objects.filter(gameCategories__category__icontains ='Action' )
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'store.html', {'returnedGames': returnedGames, 'user': user, 'search': 'War'})
    return render(request, 'store.html', {'returnedGames': returnedGames, 'search': 'War'})

@csrf_exempt
def SearchFromHomeFamily(request):
    returnedGames = Game.objects.filter(gameCategories__category__icontains ='Family') | Game.objects.filter(gameCategories__category__icontains ='children' ) | Game.objects.filter(gameCategories__category__icontains ='kid' )
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'store.html', {'returnedGames': returnedGames, 'user': user, 'search': 'Family'})
    return render(request, 'store.html', {'returnedGames': returnedGames, 'search': 'Family'})

@csrf_exempt
def SearchFromHomePS5(request):
    returnedGames = Game.objects.filter(platforms__platformName__icontains = 'PS5')
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'store.html', {'returnedGames': returnedGames, 'user': user,'search': 'Playstation 5'})
    return render(request, 'store.html', {'returnedGames': returnedGames, 'search': 'Playstation 5'})


@csrf_exempt
def SearchFromHomePromotion(request):
    game_promotions = GamePromotion.objects.all().select_related('game')
    returnedGames = []

    for game_promotion in game_promotions:
        game = game_promotion.game
        returnedGames.append(game)

    if request.user.is_authenticated:
        user = request.user
        return render(request, 'store.html', {'returnedGames': returnedGames, 'user': user, 'search': 'Promotion'})
    return render(request, 'store.html', {'returnedGames': returnedGames, 'search': 'Promotion'})


@csrf_exempt
def SearchFromHomePlatform(request):
    returnedGames = Game.objects.filter(platforms__platformName__icontains ='Family')
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'store.html', {'returnedGames': returnedGames, 'user': user})
    return render(request, 'store.html', {'returnedGames': returnedGames})

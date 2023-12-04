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

        if not platform_to_search and not genre_to_search:

            result = Game.objects.all()
            serializer = GameSerializer(result, many=True)
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
                result = genre_to_search_result
            elif not genre_to_search:
                result = platform_to_search_result
            else:
                # Find the common elements
                common_elements = set(platform_to_search_result).intersection(set(genre_to_search_result))
                result = list(common_elements)


            # Perform filtering based on selected platforms in your model/queryset
            # Example: filtered_data = YourModel.objects.filter(platform__in=selected_platforms)
            #result = Game.objects.filter(platforms__in=selected_platforms)
            #games = Game.objects.filter(platforms__platformName__in=selected_platforms).values('name', 'price', 'description', 'releaseDate', 'platforms__platformName')

            # Convert queryset to a list of dictionaries
            #games_list = list(games)
            serializer = GameSerializer(result, many=True)
            json_data = serializer.data

            # Return filtered data as JSON response
            return JsonResponse({'result': json_data})

    return JsonResponse({'error': 'Invalid request method'})
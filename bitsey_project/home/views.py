from django.shortcuts import render
from django.http import HttpResponse
from browse import models as browsemodel
# Create your views here.
def home(request):
    gamesOnPromotion = browsemodel.GamePromotion.objects.all()
    print(gamesOnPromotion)
    if request.user.is_authenticated:
        user = request.user

        

        return render(request, 'index.html', {'user': user, 'gamesOnPromotion': gamesOnPromotion})

    return render(request, 'index.html', {'gamesOnPromotion': gamesOnPromotion})
    #return HttpResponse("Hello world! this i supposingly from homepahe html")
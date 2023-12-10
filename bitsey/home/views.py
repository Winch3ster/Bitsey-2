from django.shortcuts import render
from django.http import HttpResponse
from browse import models as browsemodel
# Create your views here.
def home(request):
    gamesOnPromotion = browsemodel.GamePromotion.objects.all()
    newRelease = browsemodel.NewRelease.objects.all()
    print(gamesOnPromotion)
    if request.user.is_authenticated:
        user = request.user

        return render(request, 'index.html', {'user': user, 'gamesOnPromotion': gamesOnPromotion, 'newRelease':newRelease})

    return render(request, 'index.html', {'gamesOnPromotion': gamesOnPromotion, 'newRelease':newRelease})
    #return HttpResponse("Hello world! this i supposingly from homepahe html")
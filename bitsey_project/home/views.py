from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'index.html', {'user': user})

    return render(request, 'index.html')
    #return HttpResponse("Hello world! this i supposingly from homepahe html")
from django.shortcuts import render
from user import models as usermodels
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .serializer import *
from .forms import *
from django.core.mail import send_mail

from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import redirect
from user import views as userviews
from browse import views as browseviews

# Create your views here.
@login_required
@csrf_exempt
def GetUserNotifications(request):
    if request.method == 'GET':
        user = usermodels.User.objects.get(pk=request.user.id)

        print(user)
        notificationsForUser = Notifications.objects.filter(user=user)

        serializer = NotificationsSerializer(notificationsForUser, many=True)
        json_data = serializer.data
        return JsonResponse({"notification": json_data})

@csrf_exempt
def DeleteSpecificNotification(request, notificationId):
    if request.method == 'DELETE':
        print(f"Received notification Id: {notificationId}")
        notification_to_be_deleted = Notifications.objects.get(pk = notificationId)
        notification_to_be_deleted.delete()

        #Refresh the latest notification
        user = usermodels.User.objects.get(pk=request.user.id)

        print(user)
        notificationsForUser = Notifications.objects.filter(user=user)

        serializer = NotificationsSerializer(notificationsForUser, many=True)
        json_data = serializer.data

        return JsonResponse({"status": "Success", 'notifications': json_data})

@csrf_exempt
def DeleteAllNotification(request):
    if request.method == 'DELETE':
        Notifications.objects.filter(user = request.user).delete()
        return JsonResponse({"status": "Success"})

@csrf_exempt
def ReadNotification(request):
    if request.method == 'PATCH':
        print("ReadNotification is running")
        all_user_notifications = Notifications.objects.filter(user = request.user)

        for notification in all_user_notifications:
            notification.isRead = True
            notification.save()
        
        return JsonResponse({"status": "Success"})
    
@csrf_exempt
def AnyUnreadNotification(request):
    if request.method == 'GET':
        all_user_notifications = Notifications.objects.filter(user = request.user, isRead = False)

        unreadAmount = all_user_notifications.count()

        return JsonResponse({"result": unreadAmount})




def Support(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            email = request.POST.get('email')
            message = request.POST.get('message')
        
            # CAPTCHA validation successful, handle form submission
            # Compose email message
            subject = 'Bitsey Enquiry'
            body = f'Customer Name: {first_name} {last_name}\nCustomer Email: {email}\n\nMessage:\n{message}'

            # Send email
            send_mail(subject, body, email, ["kingstonlee96@gmail.com"], fail_silently=False)

            return render(request, 'support.html', {'emailSent': True, 'form': form})
    else:
        form = SupportForm()

    return render(request, 'support.html', {'emailSent': False, 'form': form})



def BookTrial(request, game_id):
    print("Book trial is working")
    if request.method == 'POST':
        #check if user is logged in 
        #If YES, proceed 
        #If NO, redirect to front end
        if request.user.id != None:
            # set the trial date
            cGame = browsemodels.Game.objects.get(pk=game_id)
            trial = Trial(user=request.user, game = cGame, date = timezone.now(), approved= False)
            
            trial.save()
            return redirect(reverse('game_detail', args=[game_id]))
        else:
            return redirect(userviews.signin)

            
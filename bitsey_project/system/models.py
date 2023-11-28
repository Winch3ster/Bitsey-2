from django.db import models

# Create your models here.
from django.db import models
from user import models as usermodels
from browse import models as browsemodels
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from order import models as ordermodels
from datetime import date

# Create your models here.
class Notifications(models.Model):
    user = models.ForeignKey(usermodels.User, on_delete=CASCADE)
    message = models.CharField(max_length=200)
    date = models.DateField()
    isRead = models.BooleanField()

    def __str__(self):
        return self.game.name



@receiver(post_save, sender=browsemodels.GamePromotion)
def notifyGamePromotion(sender, instance, created, **kwargs):
    if created:
        # If the game is added to promotion list, go to the WishListItem tables, select all the data that has the game
        # --> Go to the wishlist --> to the user
        print(instance)

        print(instance.game)
        
        wishListItems = usermodels.WishListItem.objects.filter(game=instance.game)
        print(wishListItems)

        for item in wishListItems:
            CreateNotification(item.wishList.user, f"{item.wishList.user}, {instance.game.name} in your wishlist is on promotion!")
            print(item)
            print(item.wishList)
            print(item.wishList.user)

        print(f"{instance.game.name} is added to promotion from system model")
        # You can perform additional actions here

post_save.connect(notifyGamePromotion, sender=browsemodels.GamePromotion)


def CreateNotification(toUser, message):

    notication = Notifications(user=toUser, message = message, date=date.today(), isRead = False) 

    notication.save()

   


@receiver(post_save, sender=ordermodels.Order)
def order_shipped_notification(sender, instance, **kwargs):
    if instance.isShipped:
        print(instance.user)
        CreateIsShippedNotification(instance.user, f"Hooray! Your order (ID: {instance.id}) has been shipped!")

        print(f"An order is shipped from system model")


def CreateIsShippedNotification(toUser, message):
    notication = Notifications(user=toUser, message = message, date=date.today(), isRead = False) 

    notication.save()

post_save.connect(order_shipped_notification, sender=ordermodels.Order)
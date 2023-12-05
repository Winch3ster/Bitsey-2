from django.db import models

# Create your models here.
from django.db import models
from user import models as usermodels
from browse import models as browsemodels
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save, pre_delete
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

class Trial(models.Model):
    user = models.ForeignKey(usermodels.User, on_delete=CASCADE)
    game = models.ForeignKey(browsemodels.Game, on_delete=CASCADE)
    date = models.DateTimeField()
    approved = models.BooleanField()

    def __str__(self):
        return f"{self.user.first_name } have requested trial for  {self.game.name} on {self.date}"



@receiver(post_save, sender=browsemodels.GamePromotion)
def notifyGamePromotion(sender, instance, created, **kwargs):
    if created:
        print("Notify game promotion is running!")
        # If the game is added to promotion list, go to the WishListItem tables, select all the data that has the game
        # --> Go to the wishlist --> to the user
        print(instance)

        print(f"Instacne game: {instance.game}")
        print(f"Instance game price: {instance.game.price}")
        
        instance.oldPrice = instance.game.price
        instance.game.price = instance.newPrice 
        instance.game.isOnPromotion = True
        instance.game.save()
        instance.save()
        print(f"Instance game isOnPromotion: {instance.game.isOnPromotion}")
        print(f"Instance game oldprice: {instance.oldPrice}")

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

@receiver(pre_delete, sender=browsemodels.GamePromotion)
def game_removed_from_promotion(sender, instance, **kwargs):
    # If a Game is removed from GamePromotion
    instance.game.price = instance.oldPrice
    instance.game.isOnPromotion = False
    instance.game.save()



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
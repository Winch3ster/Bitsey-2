from django.db import models
from browse import models as browseModel
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import AbstractUser
from browse import models as browsemodels
# Create your models here.

class User(AbstractUser):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    def __str__(self):
            return (self.firstName + " " + self.lastName)

class Address(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    streetLine1 = models.CharField(max_length=100)
    streetLine2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postalCode = models.IntegerField()
    country = models.CharField(max_length=25)



class UserWishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    game = models.ManyToManyField(browsemodels.Game, through='WishListItem')

    def __str__(self):
        return f"Wishlist for {self.user.username}"



class WishListItem(models.Model):
    wishList = models.ForeignKey(UserWishList, on_delete=models.CASCADE)
    game = models.ForeignKey(browsemodels.Game, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.game} in {self.wishList}"










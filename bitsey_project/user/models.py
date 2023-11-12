from django.db import models
from browse import models as browseModel
from django.db.models.deletion import CASCADE

# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    username = models.CharField(max_length=50 )
    email = models.EmailField(max_length = 254, blank=True, unique=True)
    password = models.CharField(max_length=50)

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






















class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    subtotal = models.FloatField()
    total = models.FloatField()
    games = models.ManyToManyField(browseModel.Game)



class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(browseModel.Game)
from django.db import models

# Create your models here.

class Platform(models.Model):
    platformName = models.CharField(max_length=20)

class GameplayImage(models.Model):
    gameplayImageURL = models.CharField(max_length=100)

class GameCategory(models.Model):
    category = models.CharField(max_length=30)



class Game(models.Model):
    #By default, Django automatically add id to each instance
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    publisher = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    releaseDate = models.DateField()
    imageURL = models.CharField(max_length=100)

    platforms = models.ManyToManyField(Platform)
    gameCategories = models.ManyToManyField(GameCategory)
    gameplayImages = models.ManyToManyField(GameplayImage)

class User(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length = 254, blank=True, unique=True)
    password = models.CharField(max_length=50)


class Address(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
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
    games = models.ManyToManyField(Game)



class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)
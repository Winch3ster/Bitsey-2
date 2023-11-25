from django.db import models
from django.db.models.deletion import CASCADE
# Create your models here.



class Platform(models.Model):
    platformName = models.CharField(max_length=20)

    def __str__(self):
        return self.platformName

class GameCategory(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category

class GameCapabilities(models.Model):
    description = models.CharField(max_length=20)
    def __str__(self):
            return self.description

class Game(models.Model):
    #By default, Django automatically add id to each instance
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    publisher = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    releaseDate = models.DateField()
    physicalCopyQuantity = models.IntegerField()
    
    #gameDirectory = name
    #parentDirectory = '../static/images/game/'
    #path = os.path.join(parentDirectory, gameDirectory)
    #os.mkdir(path)

    image = models.ImageField(upload_to= 'images/game')

    platforms = models.ManyToManyField(Platform)
    gameCategories = models.ManyToManyField(GameCategory)
    gameCapabilities = models.ManyToManyField(GameCapabilities)

    def __str__(self):
        return self.name
    
class GameplayImage(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gameplay_images', null=True, blank=True)
    #parentDirectory = '../static/images/game/'
    gameplayImage = models.ImageField(upload_to='images/game/gameplayImages/')



class GamePromotion(models.Model):
    game = models.ForeignKey(Game, on_delete=CASCADE)
    newPrice = models.FloatField()


class PreOrderGame(models.Model):   
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    publisher = models.CharField(max_length=100)
    developer = models.CharField(max_length=100)
    releaseDate = models.DateField()
    image = models.ImageField(upload_to= 'images/game')
    platforms = models.ManyToManyField(Platform)
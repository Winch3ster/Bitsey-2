from django.db import models
from user import models as usermodels
from browse import models as browsemodels
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(usermodels.User, on_delete=models.CASCADE)
    game = models.ManyToManyField(browsemodels.Game, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"



class CartItem(models.Model):
    physical = "physical"
    digital = "digital"

    EDITIONS = ((physical, "physical"), 
    (digital, "digital"))

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    game = models.ForeignKey(browsemodels.Game, on_delete=models.CASCADE)
    edition = models.CharField(
        max_length=8,
        choices=EDITIONS,
        default=digital
    )
    platform = models.CharField( 
        max_length=20
        )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.game.name} in {self.cart}"
    


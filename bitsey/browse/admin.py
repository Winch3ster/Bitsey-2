from django.contrib import admin
from .models import *
from order import models as ordermodels
from system import models as sysmodels

# Register your models here.
#admin.site.register(Game)
admin.site.register(Platform)
admin.site.register(GameCategory)
admin.site.register(GameCapabilities)


class GameplayImageAdmin(admin.StackedInline):
    model = GameplayImage

class GameAdmin(admin.ModelAdmin):
    inlines = [GameplayImageAdmin]
    exclude = ('isOnPromotion',)

    class Meta:
        model = Game

class OrderAdmin(admin.ModelAdmin):
    # Specify the fields you want to be editable in the admin interface
    fields = ['isShipped']

    # Customize display fields in the list view
    list_display = ['user', 'totalPrice', 'orderDate']

class GamePromotionAdmin(admin.ModelAdmin):
    exclude = ('oldPrice',)

admin.site.register(GamePromotion, GamePromotionAdmin)



# Register the model with the custom admin class
admin.site.register(ordermodels.Order, OrderAdmin)

#admin.site.register(GameplayImage)
admin.site.register(Game, GameAdmin)



class TrialAdmin(admin.ModelAdmin):
    # the fields to be editable in the admin interface
    fields = ['approved']

    # Customize display fields in the list view
    list_display = ['user', 'game', 'date']


admin.site.register(sysmodels.Trial, TrialAdmin)
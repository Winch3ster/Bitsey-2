from django.contrib import admin
from .models import *
# Register your models here.
#admin.site.register(Game)
admin.site.register(Platform)
admin.site.register(GameCategory)
admin.site.register(GameCapabilities)
admin.site.register(GamePromotion)

class GameplayImageAdmin(admin.StackedInline):
    model = GameplayImage

class GameAdmin(admin.ModelAdmin):
    inlines = [GameplayImageAdmin]

    class Meta:
        model = Game

#admin.site.register(GameplayImage)
admin.site.register(Game, GameAdmin)
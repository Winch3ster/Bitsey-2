from django.contrib import admin
from browse import models
# Register your models here.
admin.site.register(models.Game)
admin.site.register(models.Platform)
admin.site.register(models.GameCategory)
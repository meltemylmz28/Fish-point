from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FishingSpot, FishSpecies, SpotFishRelation

admin.site.register(FishingSpot)
admin.site.register(FishSpecies)
admin.site.register(SpotFishRelation)
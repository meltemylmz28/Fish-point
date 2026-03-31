from rest_framework import serializers
from .models import FishingSpot, FishSpecies, SpotFishRelation


class FishingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishingSpot
        fields = ['id', 'name', 'district', 'lat', 'lng', 'description']


class FishSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishSpecies
        fields = ['id', 'name', 'min_pressure', 'max_pressure', 'min_temp', 'max_temp',
                  'best_season', 'bait', 'rod', 'line']


class SpotFishRelationSerializer(serializers.ModelSerializer):
    spot_name = serializers.ReadOnlyField(source='spot.name')
    fish_name = serializers.ReadOnlyField(source='fish.name')

    class Meta:
        model = SpotFishRelation
        fields = ['id', 'spot', 'spot_name', 'fish', 'fish_name', 'abundance']
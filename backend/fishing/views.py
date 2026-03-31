from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import FishingSpot, FishSpecies, SpotFishRelation
from .serializers import FishingSpotSerializer, FishSpeciesSerializer, SpotFishRelationSerializer

class SpotListView(generics.ListAPIView):
    queryset = FishingSpot.objects.all()
    serializer_class = FishingSpotSerializer
    permission_classes = [AllowAny]

class SpotDetailView(generics.RetrieveAPIView):
    queryset = FishingSpot.objects.all()
    serializer_class = FishingSpotSerializer
    permission_classes = [AllowAny]

class FishSpeciesListView(generics.ListAPIView):
    queryset = FishSpecies.objects.all()
    serializer_class = FishSpeciesSerializer
    permission_classes = [AllowAny]
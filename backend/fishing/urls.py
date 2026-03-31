from django.urls import path
from . import views

urlpatterns = [
    path('spots/', views.SpotListView.as_view(), name='spot-list'),
    path('spots/<int:pk>/', views.SpotDetailView.as_view(), name='spot-detail'),
    path('fish/', views.FishSpeciesListView.as_view(), name='fish-list'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('spots/', views.SpotListView.as_view(), name='spot-list'),
    path('spots/<int:pk>/', views.SpotDetailView.as_view(), name='spot-detail'),
    path('fish/', views.FishSpeciesListView.as_view(), name='fish-list'),
    # 'api/' önekini buradan kaldır, çünkü core/urls.py zaten bunu karşıladı
    path('advice/<int:spot_id>/', views.get_fishing_advice, name='fishing-advice'),
    path('weather/', views.get_weather_for_coords, name='weather-by-coords'),
    path('spots-by-fish/', views.spots_by_fish, name='spots-by-fish'),
]
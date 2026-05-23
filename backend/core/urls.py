from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/fishing/', include('fishing.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/users/', include('users.urls')),
]
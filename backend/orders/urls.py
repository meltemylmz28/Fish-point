from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('orders/', views.OrderCreateView.as_view(), name='order-create'),
    path('admin/orders/', views.OrderListView.as_view(), name='order-list'),
]
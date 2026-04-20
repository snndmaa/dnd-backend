from django.urls import path

from .views import PropertyDetailAPIView, PropertyListAPIView

urlpatterns = [
    path('properties/', PropertyListAPIView.as_view(), name='property_list'),
    path('properties/<int:pk>/', PropertyDetailAPIView.as_view(), name='property_detail'),
]

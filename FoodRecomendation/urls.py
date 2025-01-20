# FoodRecomendation/urls.py

from django.urls import path
from .views import meal

urlpatterns = [
    path('meal/', meal, name='meal'),
]

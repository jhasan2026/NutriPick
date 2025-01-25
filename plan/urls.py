from django.urls import path
from . import views

app_name = 'plan'

urlpatterns = [
    path('', views.workout_plan, name='workout_plan'),
]

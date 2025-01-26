from django.urls import path
from . import views

urlpatterns = [
    path('', views.plan_home, name='plan_home'),  # Root URL for /plan/
]

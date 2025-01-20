from django.urls import path
from . import views

urlpatterns = [
    path('', views.workout_plan, name='workout_plan'),
    path('add_task/', views.add_task, name='add_task'),
    path('update_task/<int:task_id>/', views.update_task, name='update_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
]

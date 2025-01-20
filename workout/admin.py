from django.contrib import admin
from .models import workoutRoutine, Event
# Register your models here.

admin.site.register(workoutRoutine)
admin.site.register(Event)

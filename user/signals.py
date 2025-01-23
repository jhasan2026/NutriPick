from .models import Patient
from django.db.models.signals import post_save
from django.dispatch import receiver
from workout.models import workoutRoutine

@receiver(post_save, sender=Patient)
def create_student(sender, instance, created, **kwargs):
    if created:
        workoutRoutine.objects.create(user=instance.user)

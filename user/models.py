from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    gender = models.CharField(default='',max_length=8)
    height = models.FloatField(default=0.0)
    weight = models.FloatField(default=0.0)
    activity_level = models.CharField(default="",max_length=20)
    bio = models.CharField(default='',max_length=200)
    image = models.ImageField(default='default.jpg',upload_to='profile_pc')
    location = models.CharField(default='',max_length=100)
    phone_number = models.CharField(default='',max_length=15)

    def __str__(self):
        return f"{self.user.username}'s Profile"


    @receiver(post_save, sender=User)
    def create_or_update_patient_profile(sender, instance, created, **kwargs):
        if created:
            Patient.objects.create(user=instance)


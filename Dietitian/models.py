from django.db import models
from user.models import User, Patient
from datetime import datetime
# Create your models here.

class Dietitian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    gender = models.CharField(default='', max_length=8)
    qualifications = models.TextField(default='', blank=True, null=True)
    years_of_experience = models.IntegerField(default=0)
    specialties = models.CharField(default='', max_length=200, blank=True, null=True)
    bio = models.CharField(default='', max_length=300, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='dietitian_pictures/')
    location = models.CharField(default='', max_length=100, blank=True, null=True)
    phone_number = models.CharField(default='', max_length=15, blank=True, null=True)
    dob = models.DateTimeField(default=datetime.now)
    availability = models.CharField(default='', max_length=200, blank=True, null=True)
    consultation_fee = models.FloatField(default=0.0)

    def __str__(self):
        return f"Dietitian: {self.user.first_name} {self.user.last_name}"


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dietitian = models.ForeignKey(Dietitian, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField(default=datetime.now)
    status = models.CharField(
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Pending',
        max_length=10
    )
    reason_for_visit = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(default='', blank=True, null=True)
    follow_up_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Appointment with {self.dietitian.user.first_name} for {self.patient.user.first_name} on {self.appointment_date}"

    class Meta:
        ordering = ['appointment_date']



from django.db import models
from user.models import User
from datetime import time,date
# Create your models here.

class workoutRoutine(models.Model):
    sat_time_start = models.TimeField(default=time(12, 0),null=True)
    sun_time_start = models.TimeField(default=time(12, 0),null=True)
    mon_time_start = models.TimeField(default=time(12, 0),null=True)
    tue_time_start = models.TimeField(default=time(12, 0),null=True)
    wed_time_start = models.TimeField(default=time(12, 0),null=True)
    thu_time_start = models.TimeField(default=time(12, 0),null=True)
    fri_time_start = models.TimeField(default=time(12, 0),null=True)


    sat_time_end = models.TimeField(default=time(12, 0),null=True)
    sun_time_end = models.TimeField(default=time(12, 0),null=True)
    mon_time_end = models.TimeField(default=time(12, 0),null=True)
    tue_time_end = models.TimeField(default=time(12, 0),null=True)
    wed_time_end = models.TimeField(default=time(12, 0),null=True)
    thu_time_end = models.TimeField(default=time(12, 0),null=True)
    fri_time_end = models.TimeField(default=time(12, 0),null=True)

    sat_work = models.CharField(max_length=10,default='No')
    sun_work = models.CharField(max_length=10,default='No')
    mon_work = models.CharField(max_length=10,default='No')
    tue_work = models.CharField(max_length=10,default='No')
    wed_work = models.CharField(max_length=10,default='No')
    thu_work = models.CharField(max_length=10,default='No')
    fri_work = models.CharField(max_length=10,default='No')

    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)



    def __str__(self):
        return f'{self.user.username} Plan'

class Event(models.Model):
    title = models.CharField(max_length=100)  # Field for the event title
    details = models.TextField(max_length=500,default='',null=True,blank=True)  # Field for additional details of the event
    event_date = models.DateField(default=date.today,null=True,blank=True)
    starting_time = models.TimeField(null=True,blank=True)  # Field for event start time
    ending_time = models.TimeField(null=True,blank=True)  # Field for event end time

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
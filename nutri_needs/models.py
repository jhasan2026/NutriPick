from django.db import models

class UserInput(models.Model):
    text = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]  


class CustomerData(models.Model):
    age = models.PositiveIntegerField()
    height_foot = models.PositiveIntegerField()
    height_inch = models.PositiveIntegerField()
    weight = models.FloatField()
    respiratory_problem = models.BooleanField(default=False)
    diabetics = models.BooleanField(default=False)
    high_blood_pressure = models.BooleanField(default=False)
    heart_problem = models.BooleanField(default=False)
    constipation = models.BooleanField(default=False)
    other_conditions = models.TextField(blank=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

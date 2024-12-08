from django.db import models

class UserInput(models.Model):
    text = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]  # Show the first 50 characters

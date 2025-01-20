from django import forms
from .models import Appointment,Dietitian

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['dietitian', 'appointment_date', 'reason_for_visit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dietitian'].queryset = Dietitian.objects.all()

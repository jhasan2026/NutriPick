from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Appointment, Dietitian
from user.models import Patient
from datetime import datetime

@login_required
def book_appointment(request):
    if request.method == 'POST':
        dietitian_id = request.POST.get('dietitian')
        appointment_date = request.POST.get('appointment_date')
        reason_for_visit = request.POST.get('reason_for_visit')

        if not dietitian_id or not appointment_date:
            return render(request, 'book_appointment.html', {'error': 'All fields are required.'})

        try:
            dietitian = Dietitian.objects.get(id=dietitian_id)
        except Dietitian.DoesNotExist:
            raise Http404("Dietitian not found")

        # Create the Appointment object
        patient = Patient.objects.get(user=request.user)
        appointment = Appointment.objects.create(
            patient=patient,
            dietitian=dietitian,
            appointment_date=datetime.strptime(appointment_date, '%Y-%m-%dT%H:%M'),
            reason_for_visit=reason_for_visit
        )

        return redirect('appointments')

    # Fetch dietitians for the dropdown
    dietitians = Dietitian.objects.all()
    return render(request, 'Dietitian/book_appointment.html', {'dietitians': dietitians})


@login_required
def view_appointments(request):
    patient = Patient.objects.get(user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
    return render(request, 'Dietitian/appointments_list.html', {'appointments': appointments})


@login_required
def confirm_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if appointment.dietitian.user == request.user:  # Only dietitian can confirm
        appointment.status = 'Confirmed'
        appointment.save()
    return redirect('appointments')



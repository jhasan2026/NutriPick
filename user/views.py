import pandas as pd
from django.shortcuts import render
from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from .models import Patient
from .forms import PatientProfileUpdateForm,UserUpdateForm
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
# Create your views here.
import pandas as pd
import joblib
BMI_preprocessor = joblib.load('CaloryPredictionModel/BMR_Preprocessor')
BMI_predictor = joblib.load('CaloryPredictionModel/BMI_predictor')

BMR_predictor = joblib.load('CaloryPredictionModel/BMR_predictor')

Calory_Need_Preprocessor = joblib.load('CaloryPredictionModel/Calory_Need_Preprocessor')
Calory_Need_Predictor = joblib.load('CaloryPredictionModel/Calory_Need_Predictor')


def home(request):
    return render(request,'user/BASE.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # Log the user in and redirect to the homepage
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, 'Something went wrong during authentication')
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'user/register.html')


class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        # print(self.request.POST)  # Print the POST data for debugging
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('home')


def profile_update_view(request):
    # Get the user's profile instance
    patient = get_object_or_404(Patient, user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # User update form
        profile_update_form = PatientProfileUpdateForm(request.POST, request.FILES, instance=patient)  # Profile update form

        # Extracting the date of birth from the form
        dob = datetime.strptime(profile_update_form['dob'].value(), "%Y-%m-%d").date()

        # Current date
        today = datetime.today().date()

        # Calculate the age
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        height = float(profile_update_form['height'].value())


        weight = float(profile_update_form['weight'].value())


        activity_level = float(profile_update_form['activity_level'].value())


        gender = profile_update_form['gender'].value()


        newData = [age,weight,gender,height,activity_level]
        col_names = ['age', 'weight(kg)','gender', 'height(m)','activity_level']

        newData_Df = pd.DataFrame([newData],columns=col_names)
        newData_Df_trf = BMI_preprocessor.transform(newData_Df)


        BMI_pred = BMI_predictor.predict(newData_Df_trf)
        BMR_pred = BMR_predictor.predict(newData_Df_trf)

        newData_cal = [age, weight, gender, height, activity_level,BMI_pred,BMI_pred]
        col_names_cal = ['age', 'weight(kg)', 'gender', 'height(m)', 'activity_level','BMI','BMR']

        newData_Df_cal = pd.DataFrame([newData_cal], columns=col_names_cal)
        newData_Df_trf_cal = Calory_Need_Preprocessor.transform(newData_Df_cal)

        calories_need = Calory_Need_Predictor.predict(newData_Df_trf_cal)

        if user_form.is_valid() and profile_update_form.is_valid():
            patient.bmi = BMI_pred[0]
            patient.bmr = BMR_pred[0]
            patient.calories_need = calories_need[0]
            user_form.save()
            profile_update_form.save()
            patient.save()
            return redirect('profile')
        else:
            print(user_form.errors)
            print(profile_update_form.errors)

    else:
        user_form = UserUpdateForm(instance=request.user)  # Load existing user instance
        profile_update_form = PatientProfileUpdateForm(instance=patient)  # Load existing profile instance

    return render(request, 'user/profile.html', {
        'user_form': user_form,
        'profile_form': profile_update_form,
        'patient': patient,
    })









from django.shortcuts import render, redirect
from .models import Patient


def set_default_image_view(request, patient_id):
    # Get the patient's instance
    patient = Patient.objects.get(id=patient_id)

    # Set the default image if no image exists
    if not patient.image:
        patient.image = 'profile_pics/default.jpg'
        patient.save()

    # Redirect to the profile page or another page
    return redirect('profile')

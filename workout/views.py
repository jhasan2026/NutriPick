from datetime import timedelta, time, datetime
from .models import workoutRoutine, Event
from django.shortcuts import render, redirect
import pandas as pd
import joblib
from user.models import User,Patient
Calory_Burn_preprocessor = joblib.load('CaloryPredictionModel/Calory_Burn_Preprocessor')
Calory_Burn_predictor = joblib.load('CaloryPredictionModel/Calory_Burn_Predictor')
from django.contrib.auth.decorators import login_required

def parse_time(time_string):
    if time_string:
        try:
            return datetime.strptime(time_string, "%H:%M").time()
        except ValueError:
            return None
    return None

@login_required
def workout_plan(request):
    if request.method == 'POST':
        sat_time_start = request.POST.get('start-time-saturday')
        sun_time_start = request.POST.get('start-time-sunday')
        mon_time_start = request.POST.get('start-time-monday')
        tue_time_start = request.POST.get('start-time-tuesday')
        wed_time_start = request.POST.get('start-time-wednesday')
        thu_time_start = request.POST.get('start-time-thursday')
        fri_time_start = request.POST.get('start-time-friday')

        sat_time_end = request.POST.get('end-time-saturday')
        sun_time_end = request.POST.get('end-time-sunday')
        mon_time_end = request.POST.get('end-time-monday')
        tue_time_end = request.POST.get('end-time-tuesday')
        wed_time_end = request.POST.get('end-time-wednesday')
        thu_time_end = request.POST.get('end-time-thursday')
        fri_time_end = request.POST.get('end-time-friday')


        # Update the workout routine for the logged-in user
        weekly_workout, created = workoutRoutine.objects.update_or_create(
            user=request.user,
            defaults={
                'sat_time_start': parse_time(sat_time_start),
                'sun_time_start': parse_time(sun_time_start),
                'mon_time_start': parse_time(mon_time_start),
                'tue_time_start': parse_time(tue_time_start),
                'wed_time_start': parse_time(wed_time_start),
                'thu_time_start': parse_time(thu_time_start),
                'fri_time_start': parse_time(fri_time_start),

                'sat_time_end': parse_time(sat_time_end),
                'sun_time_end': parse_time(sun_time_end),
                'mon_time_end': parse_time(mon_time_end),
                'tue_time_end': parse_time(tue_time_end),
                'wed_time_end': parse_time(wed_time_end),
                'thu_time_end': parse_time(thu_time_end),
                'fri_time_end': parse_time(fri_time_end),

                'sat_work': request.POST.get('sat_work'),
                'sun_work': request.POST.get('sun_work'),
                'mon_work': request.POST.get('mon_work'),
                'tue_work': request.POST.get('tue_work'),
                'wed_work': request.POST.get('wed_work'),
                'thu_work': request.POST.get('thu_work'),
                'fri_work': request.POST.get('fri_work'),
            }
        )


        # Fetch the updated workout data
        workout_data = workoutRoutine.objects.filter(user=request.user).first()

        context = {'workout_data': workout_data}
        return render(request, 'workout/workout_plan.html', context)

    def time_difference_in_hours(time1, time2):
        delta1 = timedelta(hours=time1.hour, minutes=time1.minute, seconds=time1.second)
        delta2 = timedelta(hours=time2.hour, minutes=time2.minute, seconds=time2.second)

        # Calculate the absolute difference
        time_difference = abs(delta1 - delta2)

        # Convert to hours
        return round(time_difference.total_seconds() / 3600,1)


    workout_data = workoutRoutine.objects.filter(user=request.user).first()
    print(workout_data.sat_time_start)

    hour_info = {
        'sat_duration':  time_difference_in_hours(workout_data.sat_time_end,workout_data.sat_time_start),
        'sun_duration':  time_difference_in_hours(workout_data.sun_time_end,workout_data.sun_time_start),
        'mon_duration':  time_difference_in_hours(workout_data.mon_time_end,workout_data.mon_time_start),
        'tue_duration':  time_difference_in_hours(workout_data.tue_time_end,workout_data.tue_time_start),
        'wed_duration':  time_difference_in_hours(workout_data.wed_time_end,workout_data.wed_time_start),
        'thu_duration':  time_difference_in_hours(workout_data.thu_time_end,workout_data.thu_time_start),
        'fri_duration':  time_difference_in_hours(workout_data.fri_time_end,workout_data.fri_time_start),
    }

    user = request.user
    profile = Patient.objects.get(user=user)
    work_data = workoutRoutine.objects.get(user=user)

    dob = profile.dob
    today = datetime.today().date()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    height = float(profile.height)
    weight = float(profile.weight)
    bmi = float(profile.bmi)
    gender = profile.gender.capitalize()


    col_names = ['Age','Gender','Weight (kg)','Height (m)','Session_Duration (hours)','Workout_Type','BMI']


    # Initialize predictions for each day
    predictions = {
        'sat': 0,
        'sun': 0,
        'mon': 0,
        'tue': 0,
        'wed': 0,
        'thu': 0,
        'fri': 0
    }

    # List of days to iterate over
    days = ['sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri']

    for day in days:
        # Construct dynamic variables for the day
        work_day = getattr(work_data, f'{day}_work')  # e.g., work_data.sat_work
        duration = hour_info.get(f'{day}_duration', 0)  # e.g., hour_info['sat_duration']

        if work_day != 'No' and duration != 0:
            # Wrap data in a list to create a valid DataFrame
            newData = [[age, gender, weight, height, duration, work_day, bmi]]
            newData_df = pd.DataFrame(newData, columns=col_names)

            # Transform and predict
            newData_trf = Calory_Burn_preprocessor.transform(newData_df)
            predictions[day] = round(Calory_Burn_predictor.predict(newData_trf)[0],1)

    print(predictions)

    eventList = Event.objects.filter(user=request.user).order_by('-created_at')


    return render(request, 'workout/workout_plan.html', {
        'workout_data': workout_data,
        'hour_info':hour_info,
        'predictions':predictions,
        'eventList':eventList
    })

@login_required
def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details')
        event_date = request.POST.get('event_date')
        starting_time = request.POST.get('starting_time')
        ending_time = request.POST.get('ending_time')

        starting_time = parse_time(starting_time)
        ending_time = parse_time(ending_time)
        event_date_obj = datetime.strptime(event_date, "%Y-%m-%d").date()

        event_create = Event.objects.create(
            title=title,
            details=details,
            event_date=event_date,
            starting_time=starting_time,
            ending_time=ending_time,
            user = request.user
        )
        event_create.save()
        return redirect('workout_plan')

    return render(request,template_name='workout/add_task.html')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Event
from datetime import datetime

@login_required
def update_task(request, task_id):
    # Fetch the task that needs to be updated
    task = get_object_or_404(Event, id=task_id, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details')
        event_date = request.POST.get('event_date')
        starting_time = request.POST.get('starting_time')
        ending_time = request.POST.get('ending_time')

        starting_time = parse_time(starting_time)
        ending_time = parse_time(ending_time)
        event_date_obj = datetime.strptime(event_date, "%Y-%m-%d").date()

        # Update the task fields
        task.title = title
        task.details = details
        task.event_date = event_date_obj
        task.starting_time = starting_time
        task.ending_time = ending_time
        task.save()

        return redirect('workout_plan')  # Redirect to the workout plan (task list)

    return render(request, 'workout/update_task.html', {'task': task})

@login_required
def delete_task(request, task_id):
    # Fetch the task that needs to be deleted
    task = get_object_or_404(Event, id=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('workout_plan')  # Redirect to the workout plan (task list)

    return render(request, 'workout/confirm_delete.html', {'task': task})







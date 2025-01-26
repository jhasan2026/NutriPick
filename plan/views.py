import cohere
from django.shortcuts import render

# Initialize Cohere Client
cohere_client = cohere.Client('YxmJyjufEbDJftLydW2sowne4pNRHqX54aPfk4kk')

def plan_home(request):
    if request.method == 'POST':
        # Get user inputs
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        calories = request.POST.get('calories')
        purpose = request.POST.get('purpose')
        exercise_type = request.POST.get('exercise_type')
        state = request.POST.get('state')

        # Generate prompt for Cohere
        prompt = f"""Generate a 7-day workout plan for a person with the following details:
        - Height: {height} cm
        - Weight: {weight} kg
        - Daily Calorie Need: {calories}
        - Purpose: {purpose}
        - Preferred Exercise: {exercise_type}
        - Desired State: {state}

        Provide detailed plans for each day, including specific exercises, sets, reps, and times (e.g., "20 push-ups in the morning").
        give the profile first.use a format that have morning and evening twice a day and give only the exercise type the user prefers. 
        don't give any not or anything. nothing extra. I reapet no notes.
        """

        # Call Cohere API
        response = cohere_client.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=2000,
            temperature=0.7
        )

        plan_home = response.generations[0].text.strip()
        return render(request, 'plan/workout_result.html', {'plan_home': plan_home})

    return render(request, 'plan/workout_form.html')

import cohere
from django.shortcuts import render

# Initialize Cohere Client
cohere_client = cohere.Client('YxmJyjufEbDJftLydW2sowne4pNRHqX54aPfk4kk')

def plan_home(request):
    if request.method == 'POST':
        # Get user inputs
        feet = request.POST.get('feet')
        inch = request.POST.get('inch')
        weight = request.POST.get('weight')
        calories = request.POST.get('calories')
        purpose = request.POST.get('purpose')
        exercise_type = request.POST.get('exercise_type')
        state = request.POST.get('state')

        # Generate prompt for Cohere
        prompt = f"""Generate a 7-day workout plan for a person with the following details:
        - Height: {feet} feet {inch} inch
        - Weight: {weight} kg
        - Daily Calorie Need: {calories}
        - Purpose: {purpose}
        - Preferred Exercise: {exercise_type}
        - Desired State: {state}

        Provide detailed plans for each day, including specific exercises, sets, reps, and times (e.g., "20 push-ups in the morning").
        Show the profile first.
        Format the response with a daily structure, showing morning and evening sessions separately. Ensure it is focused on the preferred exercise type only. 
        No additional notes or commentary. Maintain Same template. I repeat no notes.
        """

        # Call Cohere API
        response = cohere_client.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7
        )

        plan_home = response.generations[0].text.strip()

        # Formatting the plan to make it visually appealing
        formatted_plan = format_workout_plan(plan_home)

        return render(request, 'plan/workout_result.html', {'plan_home': formatted_plan})

    return render(request, 'plan/workout_form.html')


def format_workout_plan(plan_text):
    # Function to format the output from Cohere in a structured, readable way
    
    # Remove unwanted characters (# and *) from the output
    plan_text = plan_text.replace('#', '').replace('*', '')

    plan_lines = plan_text.split('\n')
    
    # Initialize formatted plan string
    formatted_plan = '<div class="space-y-4">'
    
    # Loop through each line and create structured output
    for line in plan_lines:
        # Add basic styling for better readability
        line = line.strip()
        if line:
            if "Day" in line:  # It's the beginning of a new day
                formatted_plan += f'<h3 class="text-2xl font-semibold text-green-700">{line}</h3>'
            elif "Morning" in line or "Evening" in line:  # Sessions
                formatted_plan += f'<p class="text-lg font-medium text-gray-800">{line}</p>'
            else:  # Exercises or details
                formatted_plan += f'<p class="text-base text-gray-600">{line}</p>'
    
    formatted_plan += '</div>'

    return formatted_plan

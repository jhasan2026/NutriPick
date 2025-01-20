import re
import requests
from django.conf import settings
from django.shortcuts import render
from .forms import UserInputForm

def get_food_suggestions(data):
    # Construct the prompt using input data
    prompt = (
        f"User needs {data['daily_calories']} calories daily, "
        f"has the following diseases: {', '.join(data['diseases'])}, "
        f"and has a {data['budget']} budget. "
        f"Suggest the user a 7 day diet plan with (3 meals a day) keeping his diseases, calories count and budget in mind in Bangladeshi perspective, "
        f"It is very important that you dont give any heading or any notes or anything extra, just give the 7 day meal plan, "
        f"Use the terms Day 1,Day 2....,Breakfast, Lunch, Dinner, "
        f"Don't give any notes, Don't give any extra information, "
        f"Keep the same format everytime. "
    )

    # Send request to Cohere API for food suggestions
    response = requests.post('https://api.cohere.ai/generate', json={
        'prompt': prompt,
        'model': 'command-xlarge-nightly',
        'max_tokens': 2000,
        'temperature': 0.7
    }, headers={
        'Authorization': f'Bearer {settings.COHERE_API_KEY}'
    })

    # Check if the response is successful
    if response.status_code == 200:
        text_response = response.json().get('text', '')
        
        # Debugging: Print the raw API response
        print("Raw API Response:", text_response)
        
        # Parse meal plan and recipes from the response
        meal_plan = parse_meal_plan(text_response)
        
        return {
            'meal_plan': meal_plan,
            'original_text': text_response  # Include the original response for debugging
        }
    else:
        return {
            'meal_plan': {},
            'original_text': f"Error: {response.status_code} - {response.text}"
        }

def parse_meal_plan(text):
    meal_plan = {}
    # Extract meal plan for each day
    days = re.findall(r'Day \d+:\n([\s\S]+?)(?=Day \d+:|$)', text)
    for day_index, day_text in enumerate(days, start=1):
        meals = re.findall(r'(Breakfast|Lunch|Dinner):\s*([\s\S]+?)(?=\n(Breakfast|Lunch|Dinner):|$)', day_text)
        meal_plan[f'Day {day_index}'] = {meal[0]: meal[1].strip() for meal in meals}
    return meal_plan

def meal(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            food_suggestions = get_food_suggestions(data)
            
            # Debugging: Print the API response for inspection
            print("API Response:", food_suggestions)
            
            return render(request, 'FoodRecomendation/result.html', {
                'food_suggestions': food_suggestions
            })
    else:
        form = UserInputForm()
    return render(request, 'FoodRecomendation/meal.html', {'form': form})

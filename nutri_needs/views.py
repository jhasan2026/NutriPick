from django.shortcuts import render
from django.http import HttpResponse 
from .forms import CustomerForm
import cohere
from .forms import  CustomerForm
from .models import  CustomerData
from django.contrib import messages


# Initialize Cohere client
cohere_client = cohere.Client('qcytX68hUTdhqabTQwkdlY5IVbQhOAWHDRi0k3Nv')


def nutri_need_home(request): 
    return render(request, "nutri_needs/nutri_need_home.html")


def nutri_need_about(request): 
    return HttpResponse("hello world from about")






def analyze_data(request):
    # Get the latest customer data
    customer_data = CustomerData.objects.latest('created_at')

    # Prepare the fixed prompt with dynamic data
    diseases = []
    if customer_data.high_blood_pressure:
        diseases.append("High blood pressure")
    if customer_data.diabetics:
        diseases.append("Diabetes")
    if customer_data.heart_problem:
        diseases.append("Heart problem")
    if customer_data.constipation:
        diseases.append("Constipation")
    if customer_data.respiratory_problem:
        diseases.append("Respiratory problems")
    if customer_data.other_conditions:
        diseases.append(customer_data.other_conditions)

    disease_list = ', '.join(diseases) if diseases else "None"

    prompt = f"""
    I am {customer_data.weight} kg, {customer_data.height_foot} feet {customer_data.height_inch} inches tall, and have the following health conditions: [{disease_list}].

    I want to know:

    My ideal weight range based on my height.
    My daily calorie range to reach this ideal weight.

    Provide a detailed response that includes:

    Ideal Weight Range in kg.
    Daily Calorie Range for safe weight loss, gain, or maintain depending on the Ideal Weight Range.
    A macro and micronutrient breakdown tailored to the selected health conditions, specifically:
    Protein: Appropriate for managing diabetes, heart health, and recovery from ulcers if applicable.
    Fats: Focus on heart-healthy unsaturated fats, with adjustments for high blood pressure or heart disease.
    Carbohydrates: Incorporate low glycemic index options for diabetes and adequate fiber for constipation, if relevant.
    Fiber: Adjust to address constipation or promote heart health if applicable.
    Vitamins: Tailored recommendations based on selected diseases (e.g., B-complex for ulcers, vitamin D for respiratory health or diabetes).
    Minerals: Include specifics such as magnesium and potassium for blood pressure, iron for respiratory health, and calcium for overall wellness.

    Use this format for the answer:

    Ideal Weight Range: x-x kg

    Daily Calorie Range: x-x calories

    Daily Macro and Micronutrient Analysis:
    Protein: x grams
    Fats: x grams (focus on unsaturated fats)
    Carbohydrates: x grams (low glycemic index focus, if needed)
    Fiber: x grams
    Vitamins: Specify essential vitamins based on diseases
    Minerals: Specify essential minerals based on diseases
    note don't write anything extra outside the answer format
    """

    # Call Cohere API
    response = cohere_client.generate(
        model='command-xlarge-nightly',  
        prompt=prompt,
        max_tokens=1000
    )
    output = response.generations[0].text.strip()

    # Split response into list items
    list_items = output.split('\n')  # Split by newlines if the API format uses them
    list_items = [item.strip() for item in list_items if item.strip()]  # Remove empty or extra spaces

    return render(request, 'nutri_needs/response.html', {
        'response_list': list_items,
        'customer_data': customer_data
    })



def customer_input(request):
    if request.method == 'POST':
        # Extract data from the form
        try:
            age = int(request.POST.get('age', 0))
            height_foot = int(request.POST.get('height_foot', 0))
            height_inch = int(request.POST.get('height_inch', 0))
            weight = float(request.POST.get('weight', 0.0))
            respiratory_problem = request.POST.get('respiratory_problem') == 'on'
            diabetics = request.POST.get('diabetics') == 'on'
            high_blood_pressure = request.POST.get('high_blood_pressure') == 'on'
            heart_problem = request.POST.get('heart_problem') == 'on'
            constipation = request.POST.get('constipation') == 'on'
            other_conditions = request.POST.get('other_conditions', '')

            # Validate required fields
            if age <= 0 or height_foot <= 0 or weight <= 0.0:
                messages.error(request, 'Please enter valid data for age, height, and weight.')
                return render(request, 'nutri_needs/health_form.html')

            # Save to database
            customer = CustomerData.objects.create(
                age=age,
                height_foot=height_foot,
                height_inch=height_inch,
                weight=weight,
                respiratory_problem=respiratory_problem,
                diabetics=diabetics,
                high_blood_pressure=high_blood_pressure,
                heart_problem=heart_problem,
                constipation=constipation,
                other_conditions=other_conditions,
            )
            customer.save()
            messages.success(request, "Your data has been successfully saved.")
            return render(request, 'nutri_needs/success.html', {'customer': customer})

        except ValueError:
            messages.error(request, 'Invalid data submitted. Please check your input values.')
            return render(request, 'nutri_needs/health_form.html')

    # For GET requests, render the form
    return render(request, 'nutri_needs/health_form.html')

from django.shortcuts import render
from django.http import HttpResponse 
from .forms import UserInputForm
from .models import UserInput
from .forms import CustomerForm
import cohere


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import UserInputForm, CustomerForm
from .models import UserInput, CustomerData
import cohere

# Initialize Cohere client
cohere_client = cohere.Client('qcytX68hUTdhqabTQwkdlY5IVbQhOAWHDRi0k3Nv')


def nutri_need_home(request): 
    return render(request, "nutri_needs/nutri_need_home.html")


def nutri_need_about(request): 
    return HttpResponse("hello world from about")


def customer_input(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer_data = form.save()
            return render(request, 'nutri_needs/success.html', {'customer_data': customer_data})
    else:
        form = CustomerForm()
    return render(request, 'nutri_needs/health_form.html', {'form': form})


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
        model='command-xlarge-nightly',  # Replace with your preferred model
        prompt=prompt,
        max_tokens=1000
    )
    output = response.generations[0].text.strip()

    # Render response.html with the user data and AI response
    return render(request, 'nutri_needs/response.html', {
        'response': output,
        'customer_data': customer_data
    })




def customer_input(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer_data = form.save()
            return render(request, 'nutri_needs/success.html', {'customer_data': customer_data})
    else:
        form = CustomerForm()
    return render(request, 'nutri_needs/health_form.html', {'form': form})

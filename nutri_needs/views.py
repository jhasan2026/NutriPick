from django.shortcuts import render
from django.http import HttpResponse 
from .forms import CustomerForm
import cohere
from .forms import  CustomerForm
from .models import  CustomerData
from django.contrib import messages


from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.shortcuts import get_object_or_404












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
    list_items = output.split('\n')  
    list_items = [item.strip() for item in list_items if item.strip()]  

    # Store analysis results in the session
    request.session['analysis_results'] = list_items
    request.session['customer_data'] = {
        'age': customer_data.age,
        'height_foot': customer_data.height_foot,
        'height_inch': customer_data.height_inch,
        'weight': customer_data.weight,
        'respiratory_problem': customer_data.respiratory_problem,
        'diabetics': customer_data.diabetics,
        'high_blood_pressure': customer_data.high_blood_pressure,
        'heart_problem': customer_data.heart_problem,
        'constipation': customer_data.constipation,
        'other_conditions': customer_data.other_conditions,
    }

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

            return render(request, 'nutri_needs/success.html', {'customer': customer})

        except ValueError:
            messages.error(request, 'Invalid data submitted. Please check your input values.')
            return render(request, 'nutri_needs/health_form.html')

    # For GET requests, render the form
    return render(request, 'nutri_needs/health_form.html')



def report_pdf(request):
    # Create a Byte stream buffer
    buf = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Times-Roman", 12)

    # Fetch analysis results and customer data from the session
    list_items = request.session.get('analysis_results', [])
    customer_data = request.session.get('customer_data', None)

    if not customer_data:
        c.drawString(inch, inch, "No customer data available.")
        c.showPage()
        c.save()
        buf.seek(0)
        return FileResponse(buf, as_attachment=True, filename='report.pdf')

    # Customer data section
    textob.textLine("Customer Data:")
    textob.textLine(f"Age: {customer_data['age']}")
    textob.textLine(f"Height: {customer_data['height_foot']} feet {customer_data['height_inch']} inches")
    textob.textLine(f"Weight: {customer_data['weight']} kg")
    textob.textLine(f"Respiratory Problem: {'Yes' if customer_data['respiratory_problem'] else 'No'}")
    textob.textLine(f"Diabetes: {'Yes' if customer_data['diabetics'] else 'No'}")
    textob.textLine(f"High Blood Pressure: {'Yes' if customer_data['high_blood_pressure'] else 'No'}")
    textob.textLine(f"Heart Problem: {'Yes' if customer_data['heart_problem'] else 'No'}")
    textob.textLine(f"Constipation: {'Yes' if customer_data['constipation'] else 'No'}")
    textob.textLine(f"Other Conditions: {customer_data['other_conditions']}")
    textob.textLine("")

    # Analysis Results section
    textob.textLine("Analysis Results:")
    for item in list_items:
        textob.textLine(item)

    # Finish the PDF
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return the PDF file as a response
    return FileResponse(buf, as_attachment=True, filename='report.pdf')

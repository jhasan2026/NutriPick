from django.shortcuts import render
from django.http import HttpResponse 
from .forms import UserInputForm
from .models import UserInput
import cohere


def nutri_need_home (request): 
    return render(request,"nutri_needs/nutri_need_home.html")


def nutri_need_about (request): 
    return HttpResponse("hello world from about")



# Initialize Cohere client
cohere_client = cohere.Client('qcytX68hUTdhqabTQwkdlY5IVbQhOAWHDRi0k3Nv')

def input_page(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data['text']
            # Call Cohere API
            response = cohere_client.generate(
                model='command-xlarge-nightly',  # Replace with your preferred model
                prompt=user_text,
                max_tokens=1000
            )
            output = response.generations[0].text.strip()

            # Save to the database (optional)
            user_input = UserInput.objects.create(text=user_text, response=output)

            # Pass the response to the next page
            return render(request, 'nutri_needs/response.html', {'response': output})
    else:
        form = UserInputForm()

    return render(request, 'nutri_needs/input_page.html', {'form': form})

def show_response(request):
    return render(request, 'nutri_needs/response.html')
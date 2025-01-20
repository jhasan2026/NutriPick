# FoodRecomendation/forms.py

from django import forms

class UserInputForm(forms.Form):
    daily_calories = forms.IntegerField(label='Daily Calories Need')
    diseases = forms.MultipleChoiceField(
        choices=[
            ('diabetes', 'Diabetes'),
            ('hypertension', 'Hypertension'),
            ('heart_disease', 'Heart Disease'),
            ('high_blood_pressure', 'High Blood Pressure'),
            ('obesity', 'Obesity'),
            ('fatty_liver', 'Fatty Liver'),
            ('cholesterol', 'Cholesterol Issues'),
            ('arthritis', 'Arthritis'),
            ('thyroid', 'Thyroid Disorders'),
            ('allergies', 'Allergies'),
            # Add more diseases as needed
        ],
        widget=forms.CheckboxSelectMultiple,
        label='Diseases'
    )
    budget = forms.ChoiceField(
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High')
        ],
        label='Budget'
    )

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "space-y-6 max-w-3xl mx-auto p-6 bg-white shadow-md rounded-lg"
        self.helper.label_class = "text-lg font-semibold text-gray-700"
        self.helper.field_class = "mt-1 block w-full rounded-lg border-gray-300 shadow-sm"
        self.helper.layout = Layout(
            Field('daily_calories', css_class="p-2"),
            Field('diseases'),
            Field('budget', css_class="p-2"),
            Div(
                Submit('submit', 'Get Recommendations', css_class="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700"),
                css_class="flex justify-center"
            )
        )

    def clean_daily_calories(self):
        daily_calories = self.cleaned_data.get('daily_calories')
        
        if daily_calories is None:
            raise forms.ValidationError("This field is required.")
        
        if daily_calories <= 0:
            raise forms.ValidationError("Calories need must be a positive number.")
        
        # Optionally, set an upper limit for daily calories (e.g., 5000)
        if daily_calories > 5000:
            raise forms.ValidationError("Calories need should not exceed 5000.")
        
        return daily_calories

    def clean_diseases(self):
        diseases = self.cleaned_data.get('diseases')
        
        if not diseases:
            raise forms.ValidationError("At least one disease must be selected.")
        
        return diseases

    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        
        if not budget:
            raise forms.ValidationError("Budget is required.")
        
        return budget

from django import forms
from .models import CustomerData


class UserInputForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 4,
        'placeholder': 'Enter your text here...',
    }), label='Input Text')




class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerData
        fields = [
            'age', 'height_foot', 'height_inch', 'weight', 
            'respiratory_problem', 'diabetics', 'high_blood_pressure', 
            'heart_problem', 'constipation', 'other_conditions'
        ]
    
    other_conditions = forms.CharField(
        required=False, 
        max_length=20,
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 20}),
        help_text="Describe any other conditions (Max 500 characters)."
    )

    def clean_other_conditions(self):
        data = self.cleaned_data.get('other_conditions', '')
        if not data.isalnum() and data.strip():  # Alphanumeric check
            raise forms.ValidationError("Only alphanumeric characters are allowed.")
        return data






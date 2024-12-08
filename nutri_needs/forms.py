from django import forms

class UserInputForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 4,
        'placeholder': 'Enter your text here...',
    }), label='Input Text')

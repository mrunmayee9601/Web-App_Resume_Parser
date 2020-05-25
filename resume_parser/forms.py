from django import forms

class DocumentForm(forms.Form):
    pdf = forms.FileField(label='Upload a new resume')

class FilterForm(forms.Form):
    skills = forms.CharField(
            max_length=80,
            widget=forms.TextInput(attrs={
                "placeholder": "Skills"
            }))

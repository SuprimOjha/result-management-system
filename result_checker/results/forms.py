from django import forms
from .models import ExcelUpload

class ExcelUploadForm(forms.ModelForm):
    class Meta:
        model = ExcelUpload
        fields = ['excel_file', 'semester', 'program']


class ResultSearchForm(forms.Form):
    symbol_number = forms.CharField(
        max_length=20,
        required=True,
        label="Enter Your Symbol Number",
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., 075-BCT-1234',
            'class': 'form-control'
        })
    )
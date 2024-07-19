# forms.py
from django import forms
from .models import Image

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImagesForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        "name": "name",
        "class": "form-control",
        "placeholder": "Enter person's name"
    }))
    pic = MultipleFileField(label='Select files', required=False)
    
    class Meta:
        model = Image
        fields = ['name', 'pic']

from django import forms
from django.core.exceptions import ValidationError

from models import Universe

class CreateUniverseForm(forms.ModelForm):
    name = forms.CharField(max_length=60, required=True)
    
    class Meta:
        model=Universe
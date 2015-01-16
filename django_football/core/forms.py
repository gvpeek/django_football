from django import forms
from django.core.exceptions import ValidationError

from models import Universe

class CreateUniverseForm(forms.ModelForm):
    # name = forms.CharField(max_length=60, required=True)
    # new_players_per_year = forms.IntegerField(required=True)
    # new_player_delta_per_year = forms.IntegerField(required=False)
    
    class Meta:
        model=Universe
        fields = ['name', 'new_players_per_year', 'new_player_delta_per_year']
from django import forms
from .models import CalorieEntry

class CalorieEntryForm(forms.ModelForm):
    class Meta:
        model = CalorieEntry
        fields = ['plec', 'wiek', 'wzrost', 'waga', 'aktywnosc', 'cel']
        widgets = {
            'aktywnosc': forms.Select(choices=CalorieEntry.AKTYWNOSC_CHOICES),
        }

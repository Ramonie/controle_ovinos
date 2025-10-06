
from django import forms
from .models import Ovino

class OvinoForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        input_formats=['%d/%m/%Y', '%Y-%m-%d'],  # permite os dois formatos
        required=True
    )

    class Meta:
        model = Ovino
        fields = '__all__'
        widgets = {
            'numero_brinco': forms.TextInput(attrs={'class': 'form-control'}),
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
            'peso_atual': forms.NumberInput(attrs={'class': 'form-control'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }   
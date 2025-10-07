
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
class OvinoForm(forms.ModelForm):
    class Meta:
        model = Ovino
        fields = '__all__'
        widgets = {
            'numero_brinco': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'raca': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'sexo': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'cor': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'peso_atual': forms.NumberInput(attrs={'class': 'form-control rounded-3'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control rounded-3'}),
            'peso_ao_nascer': forms.NumberInput(attrs={'class': 'form-control rounded-3'}),
            'quantidade_crias': forms.NumberInput(attrs={'class': 'form-control rounded-3'}),
            'filiacao': forms.TextInput(attrs={'class': 'form-control rounded-3'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control rounded-3', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'foto': forms.FileInput(attrs={'class': 'form-control rounded-3'}),
        }

    def clean_numero_brinco(self):
        numero_brinco = self.cleaned_data.get('numero_brinco')

        # Se for edição, ignora o próprio objeto
        if Ovino.objects.filter(numero_brinco=numero_brinco).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("⚠️ Este número de brinco já está cadastrado.")

        return numero_brinco
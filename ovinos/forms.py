
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
from django import forms
from .models import LoteLeilao


from django import forms
from django.forms import formset_factory, BaseFormSet
from .models import Ovino, LoteLeilao


class LoteLeilaoForm(forms.ModelForm):

    ovinos = forms.ModelMultipleChoiceField(
        queryset=Ovino.objects.filter(status='Disponível').order_by('numero_brinco'),
        required=False,
        label='Selecionar animais para o lote',
        widget=forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}
        )
    )

    class Meta:
        model = LoteLeilao
        fields = [
            'numero_lote',
            'descricao',
            'preco_inicial',
            'data_leilao',
            'foto',
            'ovinos',
        ]

        widgets = {
            'numero_lote': forms.TextInput(
                attrs={'class': 'form-control rounded-3'}
            ),
            'descricao': forms.Textarea(
                attrs={'class': 'form-control rounded-3', 'rows': 3}
            ),
            'preco_inicial': forms.NumberInput(
                attrs={
                    'class': 'form-control rounded-3',
                    'step': '0.01',
                }
            ),
            'data_leilao': forms.DateInput(
                attrs={
                    'class': 'form-control rounded-3',
                    'type': 'date',
                }
            ),
            'foto': forms.ClearableFileInput(
                attrs={'class': 'form-control rounded-3'}
            ),
        }


class BaseOvinoFormSet(BaseFormSet):
    def clean(self):
        super().clean()

        if any(self.errors):
            return

        brincos = []

        for form in self.forms:
            dados = form.cleaned_data
            brinco = dados.get('numero_brinco')

            if brinco:
                if brinco in brincos:
                    raise forms.ValidationError(
                        'Não é permitido cadastrar dois animais '
                        'com o mesmo número de brinco neste lote.'
                    )
                brincos.append(brinco)


OvinoFormSet = formset_factory(
    OvinoForm,
    formset=BaseOvinoFormSet,
    extra=1,
    min_num=1,
    validate_min=True,
)
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'phone', 'photo']

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegistrarUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label="Função")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


from django import forms
from django.db.models import Q
from django.forms import formset_factory, BaseFormSet
from django.contrib.auth.models import User

from .models import (
    Ovino,
    LoteLeilao,
    Profile,
)


# ==========================================================
# FORMULÁRIO DE CADASTRO E EDIÇÃO DE OVINOS
# ==========================================================

class OvinoForm(forms.ModelForm):

    data_nascimento = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'class': 'form-control rounded-3',
                'type': 'date',
            }
        ),
        input_formats=[
            '%Y-%m-%d',
            '%d/%m/%Y',
        ],
        required=True,
    )

    class Meta:
        model = Ovino
        fields = '__all__'

        widgets = {
            'numero_brinco': forms.TextInput(
                attrs={'class': 'form-control rounded-3'}
            ),

            'raca': forms.TextInput(
                attrs={'class': 'form-control rounded-3'}
            ),

            'sexo': forms.Select(
                attrs={'class': 'form-select rounded-3'}
            ),

            'cor': forms.TextInput(
                attrs={'class': 'form-control rounded-3'}
            ),

            'peso_atual': forms.NumberInput(
                attrs={'class': 'form-control rounded-3'}
            ),

            'altura': forms.NumberInput(
                attrs={'class': 'form-control rounded-3'}
            ),

            'peso_ao_nascer': forms.NumberInput(
                attrs={'class': 'form-control rounded-3'}
            ),

            'quantidade_crias': forms.NumberInput(
                attrs={'class': 'form-control rounded-3'}
            ),

            'filiacao': forms.TextInput(
                attrs={'class': 'form-control rounded-3'}
            ),

            'status': forms.Select(
                attrs={'class': 'form-select rounded-3'}
            ),

            'foto': forms.ClearableFileInput(
                attrs={'class': 'form-control rounded-3'}
            ),
        }

    def clean_numero_brinco(self):

        numero_brinco = self.cleaned_data.get('numero_brinco')

        consulta = Ovino.objects.filter(
            numero_brinco=numero_brinco
        )

        # Na edição, ignora o próprio animal.
        if self.instance and self.instance.pk:
            consulta = consulta.exclude(
                pk=self.instance.pk
            )

        if consulta.exists():
            raise forms.ValidationError(
                'Este número de brinco já está cadastrado.'
            )

        return numero_brinco


# ==========================================================
# FORMULÁRIO DE CADASTRO E EDIÇÃO DE LOTES
# ==========================================================

class LoteLeilaoForm(forms.ModelForm):

    ovinos = forms.ModelMultipleChoiceField(
        queryset=Ovino.objects.none(),
        required=False,
        label='Selecionar animais para o lote',
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'form-check-input'
            }
        )
    )

    class Meta:
        model = LoteLeilao

        fields = [
            'numero_lote',
            'descricao',
            'preco_inicial',
            'variacao_lance',
            'data_leilao',
            'foto',
            'ovinos',
        ]

        widgets = {
            'numero_lote': forms.TextInput(
                attrs={
                    'class': 'form-control rounded-3'
                }
            ),

            'descricao': forms.Textarea(
                attrs={
                    'class': 'form-control rounded-3',
                    'rows': 3
                }
            ),

            'preco_inicial': forms.NumberInput(
                attrs={
                    'class': 'form-control rounded-3',
                    'step': '0.01',
                    'min': '0.01',
                    'placeholder': 'Ex.: 500.00'
                }
            ),

            'variacao_lance': forms.NumberInput(
                attrs={
                    'class': 'form-control rounded-3',
                    'step': '0.01',
                    'min': '0.01',
                    'placeholder': 'Ex.: 10.00'
                }
            ),

            'data_leilao': forms.DateInput(
                attrs={
                    'class': 'form-control rounded-3',
                    'type': 'date'
                }
            ),

            'foto': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control rounded-3'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Apenas animais disponíveis podem participar de um lote.
        animais = Ovino.objects.filter(
            status='Disponível'
        )

        # Se estiver editando um lote, permite manter os animais
        # que já pertencem a ele, mas impede selecionar animais
        # vinculados a qualquer outro lote.
        if self.instance and self.instance.pk:

            animais = animais.filter(
                Q(lotes__isnull=True) |
                Q(lotes=self.instance)
            )

        else:

            # No cadastro de um novo lote, somente animais
            # que ainda não pertencem a nenhum lote.
            animais = animais.filter(
                lotes__isnull=True
            )

        self.fields['ovinos'].queryset = (
            animais.distinct().order_by('numero_brinco')
        )

    def clean_preco_inicial(self):

        preco = self.cleaned_data.get('preco_inicial')

        if preco is None or preco <= 0:
            raise forms.ValidationError(
                'O preço inicial deve ser maior que zero.'
            )

        return preco

    def clean_variacao_lance(self):

        variacao = self.cleaned_data.get('variacao_lance')

        if variacao is None or variacao <= 0:
            raise forms.ValidationError(
                'A variação mínima deve ser maior que zero.'
            )

        return variacao

    def clean_ovinos(self):

        ovinos_selecionados = self.cleaned_data.get('ovinos')

        if not ovinos_selecionados:
            return ovinos_selecionados

        for animal in ovinos_selecionados:

            # Verifica se o animal pertence a outro lote.
            lotes_existentes = animal.lotes.all()

            if self.instance and self.instance.pk:
                lotes_existentes = lotes_existentes.exclude(
                    pk=self.instance.pk
                )

            if lotes_existentes.exists():

                numero_lotes = ', '.join(
                    str(lote.numero_lote)
                    for lote in lotes_existentes
                )

                raise forms.ValidationError(
                    f'O animal {animal.numero_brinco} já está '
                    f'cadastrado no(s) lote(s) {numero_lotes} '
                    'e não pode ser adicionado novamente.'
                )

        return ovinos_selecionados


# ==========================================================
# FORMSET PARA CADASTRO DE VÁRIOS OVINOS
# ==========================================================

class BaseOvinoFormSet(BaseFormSet):

    def clean(self):

        super().clean()

        if any(self.errors):
            return

        brincos = []

        for form in self.forms:

            dados = form.cleaned_data

            if not dados:
                continue

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


# ==========================================================
# FORMULÁRIO DE PERFIL
# ==========================================================

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            'role',
            'phone',
            'photo',
        ]


# ==========================================================
# FORMULÁRIO DE REGISTRO DE USUÁRIO
# ==========================================================

class RegistrarUsuarioForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Senha'
    )

    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        label='Função'
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password',
        ]

    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data['password']
        )

        if commit:
            user.save()

        return user

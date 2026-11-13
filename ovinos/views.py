
# ============================================================
# IMPORTAÇÕES
# ============================================================

from decimal import Decimal, InvalidOperation

import requests

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.db import transaction
from django.db.models import Q, Count, Max
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.db.models import Q, Count, Max, Prefetch

from .models import (
    Ovino,
    LoteLeilao,
    Lance,
    AnimalArrematado,
    Profile,
    Produtor,
)

from .forms import (
    OvinoForm,
    LoteLeilaoForm,
    ProfileForm,
)


# ============================================================
# LISTA DE OVINOS COM FILTROS
# ============================================================

# ============================================================
# LISTA DE OVINOS COM FILTROS E NOME DO COMPRADOR
# ============================================================

def lista_ovinos(request):

    query = request.GET.get('q')

    filtros = {
        'raca': request.GET.get('raca'),
        'sexo': request.GET.get('sexo'),
        'cor': request.GET.get('cor'),
        'status': request.GET.get('status'),
    }

    ovinos = Ovino.objects.all().order_by('-id')

    if query:
        ovinos = ovinos.filter(
            Q(numero_brinco__icontains=query) |
            Q(filiacao__icontains=query)
        )

    for key, value in filtros.items():
        if value:
            ovinos = ovinos.filter(**{key: value})

    # Filtros numéricos
    peso_min = request.GET.get('peso_min')
    peso_max = request.GET.get('peso_max')

    if peso_min:
        ovinos = ovinos.filter(peso_atual__gte=peso_min)

    if peso_max:
        ovinos = ovinos.filter(peso_atual__lte=peso_max)

    altura_min = request.GET.get('altura_min')
    altura_max = request.GET.get('altura_max')

    if altura_min:
        ovinos = ovinos.filter(altura__gte=altura_min)

    if altura_max:
        ovinos = ovinos.filter(altura__lte=altura_max)

    crias_min = request.GET.get('crias_min')
    crias_max = request.GET.get('crias_max')

    if crias_min:
        ovinos = ovinos.filter(quantidade_crias__gte=crias_min)

    if crias_max:
        ovinos = ovinos.filter(quantidade_crias__lte=crias_max)

    # Busca os lotes e os registros de arrematação
    lotes_com_arremates = LoteLeilao.objects.prefetch_related(
        Prefetch(
            'animalarrematado_set',
            queryset=AnimalArrematado.objects
                .select_related('usuario')
                .order_by('-data_arremate'),
            to_attr='arremates_registrados'
        )
    )

    ovinos = ovinos.prefetch_related(
        Prefetch(
            'lotes',
            queryset=lotes_com_arremates
        )
    )

    # Identifica o comprador de cada animal
    for ovino in ovinos:

        arremates = []

        for lote in ovino.lotes.all():
            arremates.extend(lote.arremates_registrados)

        if arremates:

            # Considera a arrematação mais recente
            venda = max(
                arremates,
                key=lambda item: item.data_arremate
            )

            nome_comprador = (
                venda.usuario.get_full_name().strip()
                or venda.usuario.username
            )

            ovino.comprador_nome = nome_comprador

        else:
            ovino.comprador_nome = None

    return render(
        request,
        'ovinos/lista_ovinos.html',
        {'ovinos': ovinos}
    )

# ============================================================
# ADICIONAR OVINO
# ============================================================

@login_required
def adicionar_ovino(request):

    if request.method == 'POST':
        form = OvinoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Animal cadastrado com sucesso!'
            )

            return redirect('lista_ovinos')

    else:
        form = OvinoForm()

    return render(
        request,
        'ovinos/adicionar_ovino.html',
        {'form': form}
    )


# ============================================================
# EDITAR OVINO
# ============================================================

@login_required
def editar_ovino(request, pk):

    ovino = get_object_or_404(Ovino, pk=pk)

    if request.method == 'POST':
        form = OvinoForm(
            request.POST,
            request.FILES,
            instance=ovino
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Animal atualizado com sucesso!'
            )

            return redirect('lista_ovinos')

    else:
        form = OvinoForm(instance=ovino)

    return render(
        request,
        'ovinos/editar_ovino.html',
        {
            'form': form,
            'ovino': ovino
        }
    )


# ============================================================
# DETALHES DO OVINO
# ============================================================

def detalhes_ovino(request, pk):

    ovino = get_object_or_404(Ovino, pk=pk)

    return render(
        request,
        'ovinos/detalhes_ovino.html',
        {'ovino': ovino}
    )


# ============================================================
# REMOVER OVINO
# ============================================================

@login_required
def remover_ovino(request, pk):

    ovino = get_object_or_404(Ovino, pk=pk)

    if request.method == 'POST':

        numero_brinco = ovino.numero_brinco

        ovino.delete()

        messages.success(
            request,
            f'O ovino {numero_brinco} foi removido com sucesso!'
        )

        return redirect('lista_ovinos')

    return render(
        request,
        'ovinos/confirmar_remocao.html',
        {'ovino': ovino}
    )


# ============================================================
# ATUALIZAR STATUS DO OVINO
# ============================================================

@login_required
def atualizar_status(request, pk, status):

    ovino = get_object_or_404(Ovino, pk=pk)

    status_validos = dict(Ovino.STATUS_CHOICES)

    if status in status_validos:

        ovino.status = status
        ovino.save()

        messages.success(
            request,
            f'Status do animal {ovino.numero_brinco} atualizado para '
            f'{status_validos[status]}.'
        )

    else:
        messages.error(
            request,
            'Status informado inválido.'
        )

    return redirect('lista_ovinos')


# ============================================================
# RELATÓRIOS
# ============================================================

def relatorio_disponiveis(request):

    racas = (
        Ovino.objects
        .filter(status='Disponível')
        .values('raca')
        .annotate(total=Count('id'))
    )

    sexos = (
        Ovino.objects
        .filter(status='Disponível')
        .values('sexo')
        .annotate(total=Count('id'))
    )

    return render(
        request,
        'ovinos/relatorio.html',
        {
            'racas': racas,
            'sexos': sexos
        }
    )


# ============================================================
# SAIR DO SISTEMA
# ============================================================

def sair(request):

    logout(request)

    return redirect('home')


# ============================================================
# VERIFICAR NÚMERO DO BRINCO
# ============================================================

def verificar_numero_brinco(request):

    numero_brinco = request.GET.get(
        'numero_brinco',
        ''
    ).strip()

    existe = Ovino.objects.filter(
        numero_brinco=numero_brinco
    ).exists()

    return JsonResponse({
        'existe': existe
    })


# ============================================================
# VERIFICAR NÚMERO DO LOTE
# ============================================================

def verificar_numero_lote(request):

    numero_lote = request.GET.get(
        'numero_lote',
        request.GET.get('verificar_numero_lote', '')
    ).strip()

    existe = LoteLeilao.objects.filter(
        numero_lote=numero_lote
    ).exists()

    return JsonResponse({
        'existe': existe
    })


# ============================================================
# RECUPERAÇÃO DE SENHA
# ============================================================

class CustomPasswordResetView(PasswordResetView):

    template_name = 'registration/password_reset_form.html'
    success_url = '/password_reset_done/'

    def form_valid(self, form):

        email = form.cleaned_data.get('email')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return super().form_valid(form)

        token = default_token_generator.make_token(user)

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        return redirect(
            f'/reset/{uid}/{token}/'
        )


# ============================================================
# PÁGINA PRINCIPAL DO LEILÃO
# ============================================================

def home(request):

    return leilao_view(request)


# ============================================================
# LISTAR LOTES DO LEILÃO
# ============================================================

def leilao_view(request):

    q = request.GET.get('q')

    lotes = LoteLeilao.objects.all().order_by('-id')

    if q:
        lotes = lotes.filter(
            Q(numero_lote__icontains=q) |
            Q(descricao__icontains=q)
        )

    return render(
        request,
        'ovinos/leilao_view.html',
        {'lotes': lotes}
    )


# ============================================================
# CADASTRAR LOTE
# ============================================================

@login_required
@user_passes_test(lambda u: u.is_superuser)

# ============================================================
# CADASTRAR LOTE
# ============================================================

@login_required
@user_passes_test(lambda u: u.is_superuser)
def cadastrar_lote(request):

    if request.method == 'POST':

        form = LoteLeilaoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            animais_selecionados = form.cleaned_data.get(
                'ovinos'
            )

            ids_animais = [
                animal.pk for animal in animais_selecionados
            ]

            with transaction.atomic():

                # Bloqueia os registros dos animais selecionados
                # durante a operação de cadastro.
                list(
                    Ovino.objects.select_for_update().filter(
                        pk__in=ids_animais
                    )
                )

                # Confere novamente se algum animal já foi
                # associado a outro lote.
                animais_bloqueados = Ovino.objects.filter(
                    pk__in=ids_animais,
                    lotes__isnull=False
                ).distinct()

                if animais_bloqueados.exists():

                    brincos = ', '.join(
                        str(animal.numero_brinco)
                        for animal in animais_bloqueados
                    )

                    form.add_error(
                        'ovinos',
                        'Não foi possível cadastrar o lote. '
                        f'O(s) animal(is) {brincos} já pertence(m) '
                        'a outro lote.'
                    )

                else:

                    # Salva o lote e seus animais.
                    lote = form.save()

                    quantidade = lote.ovinos.count()

                    messages.success(
                        request,
                        f'Lote cadastrado com sucesso! '
                        f'{quantidade} animal(is) associado(s).'
                    )

                    return redirect('leilao_view')

        if not form.is_valid() or form.errors:

            messages.error(
                request,
                'Não foi possível cadastrar o lote. '
                'Verifique os campos informados e os animais selecionados.'
            )

    else:

        form = LoteLeilaoForm()

    # Lista todos os animais que já pertencem a algum lote.
    # Essa lista será exibida no aviso do HTML.
    ovinos_em_lotes = (
        Ovino.objects
        .filter(lotes__isnull=False)
        .distinct()
        .prefetch_related('lotes')
        .order_by('numero_brinco')
    )

    return render(
        request,
        'ovinos/cadastrar_lote.html',
        {
            'form': form,
            'ovinos_em_lotes': ovinos_em_lotes,
        }
    )

# ============================================================
# REALIZAR LANCE
# ============================================================

@login_required
def dar_lance(request, pk):

    lote = get_object_or_404(
        LoteLeilao,
        pk=pk
    )

    if request.method == 'POST':

        with transaction.atomic():

            # Bloqueia alterações simultâneas no lote
            lote = get_object_or_404(
                LoteLeilao.objects.select_for_update(),
                pk=pk
            )

            ultimo_lance = lote.lances.order_by(
                '-valor',
                '-data_hora'
            ).first()

            valor_base = (
                ultimo_lance.valor
                if ultimo_lance
                else lote.preco_inicial
            )

            # Obtém a variação configurada no lote
            variacao = lote.variacao_lance

            valor_digitado = request.POST.get(
                'valor',
                ''
            ).strip()

            try:
                valor_escolhido = Decimal(
                    valor_digitado.replace(',', '.')
                )

                if not valor_escolhido.is_finite():
                    raise InvalidOperation

            except (InvalidOperation, ValueError):

                messages.error(
                    request,
                    'Informe um valor de lance válido.'
                )

            else:

                if lote.encerrado:

                    messages.error(
                        request,
                        'Este leilão já foi encerrado.'
                    )

                elif valor_escolhido < lote.preco_inicial:

                    messages.error(
                        request,
                        f'O lance mínimo é R$ {lote.preco_inicial:.2f}.'
                    )

                elif valor_escolhido < valor_base + variacao:

                    messages.error(
                        request,
                        f'O próximo lance deve ser de pelo menos '
                        f'R$ {valor_base + variacao:.2f}.'
                    )

                elif valor_escolhido.as_tuple().exponent < -2:

                    messages.error(
                        request,
                        'Informe no máximo duas casas decimais.'
                    )

                elif valor_escolhido > Decimal('99999999.99'):

                    messages.error(
                        request,
                        'O valor informado ultrapassa o limite permitido.'
                    )

                else:

                    Lance.objects.create(
                        lote=lote,
                        usuario=request.user,
                        valor=valor_escolhido
                    )

                    messages.success(
                        request,
                        f'Lance de R$ {valor_escolhido:.2f} '
                        f'realizado com sucesso!'
                    )

                    return redirect('leilao_view')

    # Atualiza os dados do lote e dos lances
    ultimo_lance = lote.lances.order_by(
        '-valor',
        '-data_hora'
    ).first()

    valor_base = (
        ultimo_lance.valor
        if ultimo_lance
        else lote.preco_inicial
    )

    # Obtém a variação configurada no lote
    variacao = lote.variacao_lance

    # Opções automáticas de lance
    if ultimo_lance:

        opcoes_lances = [
            valor_base + variacao * i
            for i in range(1, 7)
        ]

    else:

        opcoes_lances = [
            lote.preco_inicial + variacao * i
            for i in range(6)
        ]

    return render(
        request,
        'ovinos/dar_lance.html',
        {
            'lote': lote,
            'opcoes_lances': opcoes_lances,
            'ultimo_lance': ultimo_lance,
            'valor_base': valor_base,
            'variacao': variacao,
        }
    )

from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

@user_passes_test(lambda user: user.is_superuser)
@require_POST
def reabrir_lote(request, lote_id):

    lote = get_object_or_404(LoteLeilao, id=lote_id)

    if lote.encerrado:
        lote.encerrado = False
        lote.save(update_fields=['encerrado'])

        messages.success(
            request,
            f'O lote {lote.numero_lote} foi reaberto com sucesso!'
        )
    else:
        messages.info(
            request,
            f'O lote {lote.numero_lote} já está aberto.'
        )

    return redirect('leilao_view')

# ============================================================
# ATUALIZAR INFORMAÇÕES DO ÚLTIMO LANCE (AJAX)
# ============================================================

@login_required
def atualizar_lance(request, lote_id):

    lote = get_object_or_404(
        LoteLeilao,
        pk=lote_id
    )

    ultimo_lance = lote.lances.order_by(
        '-valor',
        '-data_hora'
    ).first()

    data = {
        'ultimo_lance': (
            float(ultimo_lance.valor)
            if ultimo_lance
            else None
        ),

        'usuario': (
            ultimo_lance.usuario.username
            if ultimo_lance
            else None
        ),
    }

    return JsonResponse(data)


# ============================================================
# ENCERRAR TODOS OS LOTES
# ============================================================

# ============================================================
# ENCERRAR TODOS OS LOTES E ATUALIZAR OS ANIMAIS VENDIDOS
# ============================================================

@login_required
@user_passes_test(lambda u: u.is_superuser)
def encerrar_leilao(request):

    lotes_ativos = LoteLeilao.objects.filter(
        encerrado=False
    )

    if not lotes_ativos.exists():

        messages.warning(
            request,
            'Nenhum lote disponível para encerrar.'
        )

        return redirect('leilao_view')

    try:

        with transaction.atomic():

            for lote in lotes_ativos:

                lance_vencedor = (
                    Lance.objects
                    .filter(lote=lote)
                    .order_by('-valor', '-data_hora')
                    .first()
                )

                if not lance_vencedor:

                    messages.warning(
                        request,
                        f'Lote {lote.numero_lote}: nenhum lance registrado. '
                        f'Os animais não foram marcados como vendidos.'
                    )

                    lote.encerrado = True
                    lote.save(update_fields=['encerrado'])

                    continue

                # Registra o comprador e o valor do arremate
                AnimalArrematado.objects.create(
                    usuario=lance_vencedor.usuario,
                    lote=lote,
                    valor_final=lance_vencedor.valor
                )

                # Atualiza todos os animais pertencentes ao lote
                lote.ovinos.update(
                    status='Vendido'
                )

                # Encerra o lote
                lote.encerrado = True
                lote.save(update_fields=['encerrado'])

        messages.success(
            request,
            'Os lotes foram encerrados e os animais arrematados '
            'foram atualizados para Vendidos!'
        )

    except Exception as e:

        messages.error(
            request,
            f'Erro ao encerrar lotes: {e}'
        )

    return redirect('leilao_view')

# ============================================================
# ENCERRAR UM LOTE INDIVIDUAL
# ============================================================

# ============================================================
# ENCERRAR LOTE INDIVIDUAL E ATUALIZAR OS ANIMAIS
# ============================================================

@login_required
@user_passes_test(lambda u: u.is_superuser)
def encerrar_leilao_individual(request, lote_id):

    with transaction.atomic():

        lote = get_object_or_404(
            LoteLeilao.objects.select_for_update(),
            pk=lote_id
        )

        if lote.encerrado:

            messages.warning(
                request,
                f'O lote {lote.numero_lote} já está encerrado.'
            )

            return redirect('leilao_view')

        lance_vencedor = (
            Lance.objects
            .filter(lote=lote)
            .order_by('-valor', '-data_hora')
            .first()
        )

        if not lance_vencedor:

            lote.encerrado = True
            lote.save(update_fields=['encerrado'])

            messages.warning(
                request,
                f'O lote {lote.numero_lote} foi encerrado, '
                f'mas não possui lances. Os animais não foram '
                f'marcados como vendidos.'
            )

            return redirect('leilao_view')

        # Registra o arremate
        AnimalArrematado.objects.create(
            usuario=lance_vencedor.usuario,
            lote=lote,
            valor_final=lance_vencedor.valor
        )

        # Atualiza todos os animais do lote
        lote.ovinos.update(
            status='Vendido'
        )

        # Encerra o lote
        lote.encerrado = True
        lote.save(update_fields=['encerrado'])

    messages.success(
        request,
        f'Lote {lote.numero_lote} arrematado por '
        f'{lance_vencedor.usuario.get_full_name() or lance_vencedor.usuario.username}! '
        f'Os animais foram atualizados para Vendidos.'
    )

    return redirect('leilao_view')

# ============================================================
# PERFIL DO USUÁRIO
# ============================================================

@login_required
def perfil(request):

    # Cria o perfil caso ainda não exista
    profile, criado = Profile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'visitor'}
    )

    lances = (
        Lance.objects
        .filter(usuario=request.user)
        .select_related('lote')
        .order_by('-data_hora')
    )

    animais = (
        AnimalArrematado.objects
        .filter(usuario=request.user)
        .select_related('lote')
        .order_by('-data_arremate')
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Perfil atualizado com sucesso!'
            )

            return redirect('perfil')

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'ovinos/perfil.html',
        {
            'form': form,
            'lances': lances,
            'animais': animais,
            'profile': profile,
        }
    )


# ============================================================
# CADASTRO DE USUÁRIO
# ============================================================

def register(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            usuario = form.save()

            # Cria o perfil inicial do usuário
            Profile.objects.get_or_create(
                user=usuario,
                defaults={'role': 'visitor'}
            )

            messages.success(
                request,
                'Cadastro realizado com sucesso! Faça seu login.'
            )

            return redirect('login')

    else:

        form = UserCreationForm()

    return render(
        request,
        'ovinos/register.html',
        {'form': form}
    )


# ============================================================
# LOGIN GOV.BR
# ============================================================

def login_govbr(request):

    url = (
        f'{settings.GOVBR_AUTH_URL}'
        f'?response_type=code'
        f'&client_id={settings.GOVBR_CLIENT_ID}'
        f'&redirect_uri={settings.GOVBR_REDIRECT_URI}'
        f'&scope=openid+profile+email'
    )

    return redirect(url)


# ============================================================
# RETORNO DA AUTENTICAÇÃO GOV.BR
# ============================================================

def callback_govbr(request):

    code = request.GET.get('code')

    if not code:

        messages.error(
            request,
            'Não foi possível obter o código de autenticação Gov.br.'
        )

        return redirect('login')

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.GOVBR_REDIRECT_URI,
        'client_id': settings.GOVBR_CLIENT_ID,
        'client_secret': settings.GOVBR_CLIENT_SECRET,
    }

    try:

        token_response = requests.post(
            settings.GOVBR_TOKEN_URL,
            data=data,
            timeout=15
        )

        token_response.raise_for_status()

        token_json = token_response.json()

        access_token = token_json.get('access_token')

        if not access_token:
            raise ValueError('Token de acesso não recebido.')

        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        user_response = requests.get(
            settings.GOVBR_USERINFO_URL,
            headers=headers,
            timeout=15
        )

        user_response.raise_for_status()

        user_data = user_response.json()

        cpf = user_data.get('sub')

        if not cpf:
            raise ValueError('CPF não recebido pelo Gov.br.')

        django_user, criado = User.objects.get_or_create(
            username=cpf,
            defaults={
                'first_name': user_data.get(
                    'name',
                    'Usuário Gov.br'
                )
            }
        )

        produtor, criado = Produtor.objects.get_or_create(
            user=django_user,
            defaults={
                'cpf': cpf,
                'nome': user_data.get(
                    'name',
                    'Usuário Gov.br'
                )
            }
        )

        Profile.objects.get_or_create(
            user=django_user,
            defaults={'role': 'visitor'}
        )

        login(request, django_user)

        return redirect('/dashboard/')

    except (
        requests.RequestException,
        ValueError,
        Produtor.DoesNotExist
    ) as e:

        messages.error(
            request,
            f'Erro na autenticação Gov.br: {e}'
        )

        return redirect('login')


# ============================================================
# HISTÓRICO DE LANCES
# ============================================================

def historico_lances(request, pk):

    lote = get_object_or_404(
        LoteLeilao,
        pk=pk
    )

    lances = (
        lote.lances
        .select_related('usuario')
        .order_by('-data_hora')
    )

    maior_lance = lote.lances.aggregate(
        maior=Max('valor')
    )['maior']

    return render(
        request,
        'lotes/historico_lances.html',
        {
            'lotes': lote,
            'lances': lances,
            'maior_lance': maior_lance,
        }
    )

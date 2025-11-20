
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ovino
from .forms import OvinoForm
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from ovinos import models

# Lista com filtros avançados
def lista_ovinos(request):
   

    query = request.GET.get('q')
    filtros = {
        'raca': request.GET.get('raca'),
        'sexo': request.GET.get('sexo'),
        'cor': request.GET.get('cor'),
        'status': request.GET.get('status'),
    }
    ovinos = Ovino.objects.all()
    if query:
        ovinos = ovinos.filter(Q(numero_brinco__icontains=query)|Q(filiacao__icontains=query))
    for key, value in filtros.items():
        if value:
            ovinos = ovinos.filter(**{key: value})
    # Filtros numéricos
    peso_min = request.GET.get('peso_min')
    peso_max = request.GET.get('peso_max')
    if peso_min: ovinos = ovinos.filter(peso_atual__gte=peso_min)
    if peso_max: ovinos = ovinos.filter(peso_atual__lte=peso_max)
    altura_min = request.GET.get('altura_min')
    altura_max = request.GET.get('altura_max')
    if altura_min: ovinos = ovinos.filter(altura__gte=altura_min)
    if altura_max: ovinos = ovinos.filter(altura__lte=altura_max)
    crias_min = request.GET.get('crias_min')
    crias_max = request.GET.get('crias_max')
    if crias_min: ovinos = ovinos.filter(quantidade_crias__gte=crias_min)
    if crias_max: ovinos = ovinos.filter(quantidade_crias__lte=crias_max)
    return render(request,'ovinos/lista_ovinos.html',{'ovinos':ovinos})
    
# Adicionar/Editar

@login_required
def adicionar_ovino(request):
    if request.method == 'POST':
        form = OvinoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_ovinos')
    else:
        form = OvinoForm()
    return render(request, 'ovinos/adicionar_ovino.html', {'form': form})

# Detalhes
def detalhes_ovino(request, pk):
    ovino = get_object_or_404(Ovino, pk=pk)
    return render(request, 'ovinos/detalhes_ovino.html', {'ovino': ovino})


# Atualizar status
@login_required
def atualizar_status(request, pk, status):
    ovino = get_object_or_404(Ovino, pk=pk)
    if status in dict(Ovino.STATUS_CHOICES).keys():
        ovino.status = status
        ovino.save()
    return redirect('lista_ovinos')

# Relatórios
def relatorio_disponiveis(request):
    racas = Ovino.objects.filter(status='Disponível').values('raca').annotate(total=Count('id'))
    sexos = Ovino.objects.filter(status='Disponível').values('sexo').annotate(total=Count('id'))
    return render(request,'ovinos/relatorio.html',{'racas':racas,'sexos':sexos})
 
@login_required
def editar_ovino(request, pk):
    ovino = get_object_or_404(Ovino, pk=pk)
    if request.method == 'POST':
        form = OvinoForm(request.POST, request.FILES, instance=ovino)
        if form.is_valid():
            form.save()
            return redirect('lista_ovinos')
    else:
        form = OvinoForm(instance=ovino)
    return render(request, 'ovinos/editar_ovino.html', {'form': form, 'ovino': ovino})



@login_required
def remover_ovino(request, pk):
    ovino = get_object_or_404(Ovino, pk=pk)
    if request.method == 'POST':
        ovino.delete()
        messages.success(request, f'O ovino {ovino.numero_brinco} foi removido com sucesso!')
        return redirect('lista_ovinos')
    return render(request, 'ovinos/confirmar_remocao.html', {'ovino': ovino})




def sair(request):
    logout(request)
    return redirect('home')  # redireciona para a página de login após sair




def verificar_numero_brinco(request):
    numero_brinco = request.GET.get('numero_brinco', None)
    existe = Ovino.objects.filter(numero_brinco=numero_brinco).exists()
    return JsonResponse({'existe': existe})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = '/password_reset_done/'

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Mesmo se o e-mail não existir, continua o fluxo padrão
            return super().form_valid(form)

        # Gera token e UID codificado
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Redireciona automaticamente para a página de redefinição
        return redirect(f'/reset/{uid}/{token}/')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Max
from django.contrib.auth.decorators import login_required
from .models import Ovino, Lance

from django.shortcuts import render
from .models import LoteLeilao

def leilao_view(request):
    q = request.GET.get('q')

    # Mostra TODOS os lotes (ativos e encerrados)
    lotes = LoteLeilao.objects.all().order_by('-id')

    if q:
        lotes = lotes.filter(
            Q(numero_lote__icontains=q) | Q(descricao__icontains=q)
        )

    return render(request, 'ovinos/leilao_view.html', {'lotes': lotes})

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import redirect
from .models import LoteLeilao, Lance, AnimalArrematado

@login_required
@user_passes_test(lambda u: u.is_superuser)
def encerrar_leilao(request):
    if request.method == 'POST':
        numero_lote = request.POST.get('numero_lote')

        try:
            # Busca todos os lotes com este número
            lotes = LoteLeilao.objects.filter(numero_lote=numero_lote)

            if not lotes.exists():
                messages.error(request, f"Nenhum lote encontrado com o número {numero_lote}.")
                return redirect('leilao_view')

            # Somente lotes não encerrados
            lotes_ativos = lotes.filter(encerrado=False)

            if not lotes_ativos.exists():
                messages.warning(request, f"O lote {numero_lote} já está encerrado.")
                return redirect('leilao_view')

            # PROCESSANDO CADA LOTE ATIVO
            for lote in lotes_ativos:
                # maior lance do lote
                lance_vencedor = Lance.objects.filter(lote=lote).order_by('-valor').first()

                if not lance_vencedor:
                    messages.warning(request, f"Lote {lote.numero_lote}: nenhum lance registrado.")
                    continue

                # Criando AnimalArrematado
                AnimalArrematado.objects.create(
                    usuario=lance_vencedor.usuario,
                    lote=lote,
                    valor_final=lance_vencedor.valor
                )

                # Encerrando o lote
                lote.encerrado = True
                lote.save()

            messages.success(request, f"Lote(s) {numero_lote} encerrado(s) e animais registrados!")

        except Exception as e:
            messages.error(request, f"Erro ao encerrar lote: {e}")

    return redirect('leilao_view')



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import LoteLeilao, Lance
from django.contrib.auth.decorators import login_required

@login_required
def dar_lance(request, pk):
    lote = get_object_or_404(LoteLeilao, pk=pk)

    # 🔹 Pega o último lance (se houver)
    ultimo_lance = lote.lances.order_by('-valor').first()

    # 🔹 Define o valor base (último lance ou preço inicial)
    valor_base = ultimo_lance.valor if ultimo_lance else lote.preco_inicial

    # 🔹 Se ainda não há lances, o primeiro valor da lista será o preço inicial
    if not ultimo_lance:
        opcoes_lances = [lote.preco_inicial] + [lote.preco_inicial + 50 * i for i in range(1, 6)]
    else:
        opcoes_lances = [valor_base + 50 * i for i in range(1, 7)]

    if request.method == 'POST':
        valor_escolhido = float(request.POST.get('valor'))

        if valor_escolhido <= valor_base and ultimo_lance:
            messages.error(request, "O valor do lance deve ser maior que o lance atual.")
        else:
            Lance.objects.create(
                lote=lote,
                usuario=request.user,
                valor=valor_escolhido
            )
            messages.success(request, f"Lance de R$ {valor_escolhido:.2f} realizado com sucesso!")
            return redirect('leilao_view')

    return render(request, 'ovinos/dar_lance.html', {
        'lote': lote,
        'opcoes_lances': opcoes_lances,
        'ultimo_lance': ultimo_lance,
    })

def historico_lances(request, pk):
    lotes = get_object_or_404(Ovino, pk=pk)
    lances = lotes.lances.order_by('-data_hora')

    maior_lance = lotes.lances.aggregate(Max('valor'))['valor__max'] or 0

    return render(request, 'lotes/historico_lances.html', {
        'lotes': lotes,
        'lances': lances,
        'maior_lance': maior_lance
    })
    
from django.http import JsonResponse
from .models import LoteLeilao, Lance

def atualizar_lance(request, lote_id):
    lote = LoteLeilao.objects.get(pk=lote_id)
    ultimo_lance = lote.lances.order_by('-valor').first()

    data = {
        'ultimo_lance': float(ultimo_lance.valor) if ultimo_lance else None,
        'usuario': ultimo_lance.usuario.username if ultimo_lance else None,
    }
    return JsonResponse(data)

    from django.shortcuts import render, redirect
from .forms import LoteLeilaoForm
from .models import LoteLeilao


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LoteLeilaoForm

@login_required
@user_passes_test(lambda u: u.is_superuser)
def cadastrar_lote(request):
    if request.method == 'POST':
        form = LoteLeilaoForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('leilao_view')
    else:
        form = LoteLeilaoForm()
    
    return render(request, 'ovinos/cadastrar_lote.html', {'form': form})

def home(request):
    return render(request, 'ovinos/home.html')

def verificar_numero_lote(request):
    numero_brinco = request.GET.get('verificar_numero_lote', None)
    existe = LoteLeilao.objects.filter(verificar_numero_lote=verificar_numero_lote).exists()
    return JsonResponse({'existe': existe})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Ovino, Lance, LoteLeilao, Profile
from .forms import ProfileForm


@login_required
def perfil(request):

    profile = request.user.profile
    lances = Lance.objects.filter(usuario=request.user)

    # pega todos os animais arrematados pelo usuário
    animais = AnimalArrematado.objects.filter(usuario=request.user).select_related('lote')

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("perfil")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "ovinos/perfil.html", {
        "form": form,
        "lances": lances,
        "animais": animais,
        "profile": profile,
    })

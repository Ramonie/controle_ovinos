
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ovino
from .forms import OvinoForm
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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


from django.contrib.auth import logout
from django.shortcuts import redirect

def sair(request):
    logout(request)
    return redirect('login')  # redireciona para a página de login após sair

from django.http import JsonResponse
from .models import Ovino

def verificar_numero_brinco(request):
    numero_brinco = request.GET.get('numero_brinco', None)
    existe = Ovino.objects.filter(numero_brinco=numero_brinco).exists()
    return JsonResponse({'existe': existe})

from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

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

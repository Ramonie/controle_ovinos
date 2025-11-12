from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from controle_ovinos import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('lista_ovinos', views.lista_ovinos, name='lista_ovinos'),
    path('adicionar/', views.adicionar_ovino, name='adicionar_ovino'),
    path('editar/<int:pk>/', views.editar_ovino, name='editar_ovino'),
    path('remover/<int:pk>/', views.remover_ovino, name='remover_ovino'),
    path('detalhes/<int:pk>/', views.detalhes_ovino, name='detalhes_ovino'),
    path('atualizar_status/<int:pk>/<str:status>/', views.atualizar_status, name='atualizar_status'),
    path('relatorios/', views.relatorio_disponiveis, name='relatorio_disponiveis'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # 🔹 Página de Leilão e Lances
    path('leilao/', views.leilao_view, name='leilao_view'),
    path('dar_lance/<int:pk>/', views.dar_lance, name='dar_lance'),
    path('historico_lances/<int:pk>/', views.historico_lances, name='historico_lances'),
    path('cadastrar_lote/', views.cadastrar_lote, name='cadastrar_lote'),
    path('encerrar_leilao/', views.encerrar_leilao, name='encerrar_leilao'),
  

    # 🔹 Verificar número do brinco (AJAX)
    path('verificar-numero-brinco/', views.verificar_numero_brinco, name='verificar_numero_brinco'),

    # 🔹 Rotas de redefinição de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='ovinos/password_reset.html'
    ), name='password_reset'),

    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='ovinos/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='ovinos/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='ovinos/password_reset_complete.html'
    ), name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
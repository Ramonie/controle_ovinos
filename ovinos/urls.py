from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.lista_ovinos, name='lista_ovinos'),
    path('adicionar/', views.adicionar_ovino, name='adicionar_ovino'),
    path('editar/<int:pk>/', views.editar_ovino, name='editar_ovino'),  # ✅ tem que ser editar_ovino
    path('remover/<int:pk>/', views.remover_ovino, name='remover_ovino'),
    path('detalhes/<int:pk>/', views.detalhes_ovino, name='detalhes_ovino'),
    path('atualizar_status/<int:pk>/<str:status>/', views.atualizar_status, name='atualizar_status'),
    path('relatorios/', views.relatorio_disponiveis, name='relatorio_disponiveis'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout')
]



from django.urls import path
from . import views


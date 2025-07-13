from django.urls import path
from . import views

app_name = 'administracao'

urlpatterns = [
    path('', views.painel_dashboard, name='painel_dashboard'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/novo/', views.cadastro_produto, name='cadastro_produto'),
    path('produtos/editar/<int:produto_id>/',
         views.editar_produto, name='editar_produto'),
    path('produtos/excluir/<int:produto_id>/',
         views.excluir_produto, name='excluir_produto'),

    # AJAX
    path('ajax/carregar-grades/',
         views.carregar_grades_por_tipo, name='carregar_grades'),
]

# src/core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('politica-trocas/', views.politica_trocas, name='politica_trocas'),
    path('politica-pagamento/', views.politica_pagamento,
         name='politica_pagamento'),
    path('contato/', views.contato, name='contato'),
    path('politica-privacidade/', views.politica_privacidade,
         name='politica_privacidade'),
    path('ofertas/', views.ofertas, name='ofertas'),
    path('novidades/', views.novidades, name='novidades'),
    # CATEGORIAS
    path('masculino/', views.masculino, name='masculino'),
    path('feminino/', views.feminino, name='feminino'),
    path('acessorios/', views.acessorios, name='acessorios'),

    # detalhe do produto
    path('produto/<int:produto_id>/',
         views.produto_detalhe, name='produto_detalhe'),

]

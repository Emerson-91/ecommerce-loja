# src/core/views.py
from django.shortcuts import render, get_object_or_404
from produtos.models import Produto, Categoria


def home(request):
    return render(request, 'core/home.html')


def sobre(request):
    return render(request, 'core/sobre.html')


def contato(request):
    # colocar logica para formulario de contato se necessario
    return render(request, 'core/contato.html')


def politica_privacidade(request):
    return render(request, 'core/politica_privacidade.html')


def ofertas(request):
    produtos = Produto.objects.filter(ativo=True).exclude(desconto_maximo=0)
    return render(request, 'core/ofertas.html', {'produtos': produtos})


def novidades(request):
    return render(request, 'core/novidades.html')

# CATEGORIAS


def masculino(request):
    produtos = Produto.objects.filter(
        ativo=True, categoria__nome__iexact='Masculino')
    return render(request, 'core/categorias/masculino.html', {'produtos': produtos})


def feminino(request):
    produtos = Produto.objects.filter(
        ativo=True, categoria__nome__iexact='Feminino')
    return render(request, 'core/categorias/feminino.html', {'produtos': produtos})


def acessorios(request):
    produtos = Produto.objects.filter(
        ativo=True, categoria__nome__iexact='Acessorios')
    return render(request, 'core/categorias/acessorios.html', {'produtos': produtos})


# -------------------detalhes produto-------------------
def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    produtos_similares = Produto.objects.filter(
        categoria=produto.categoria,
        marca=produto.marca,
        ativo=True
    ).exclude(id=produto.id)[:8]  # limitar a 8 itens

    context = {
        'produto': produto,
        'produtos_similares': produtos_similares,
    }
    return render(request, 'core/produto_detalhe.html', context)

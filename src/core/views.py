# src/core/views.py
from django.shortcuts import render, get_object_or_404
from produtos.models import Produto, Categoria


def home(request):
    produtos = Produto.objects.filter(ativo=True).order_by('-id')[:12]

    for produto in produtos:
        if produto.desconto_maximo and produto.desconto_maximo > 0:
            produto.preco_com_desconto = produto.valor_venda * \
                (1 - produto.desconto_maximo / 100)
            # 👈 ESSA LINHA FALTAVA
            produto.desconto = round(produto.desconto_maximo)
        else:
            produto.preco_com_desconto = produto.valor_venda
            produto.desconto = 0

    context = {
        'produtos': produtos,
    }
    return render(request, 'core/home.html', context)


def sobre(request):
    return render(request, 'core/sobre.html')


def politica_trocas(request):
    return render(request, 'core/politica_trocas.html')


def politica_pagamento(request):
    return render(request, 'core/politica_pagamento.html')


def sobre(request):
    return render(request, 'core/sobre.html')


def contato(request):
    # colocar logica para formulario de contato se necessario
    return render(request, 'core/contato.html')


def faq(request):
    return render(request, 'core/faq.html')


def politica_privacidade(request):
    return render(request, 'core/politica_privacidade.html')


def ofertas(request):
    produtos = Produto.objects.filter(
        ativo=True,
        desconto_maximo__gt=0
    )
    # Calcular preco_promocional e desconto para cada produto
    for p in produtos:
        p.preco_promocional = p.valor_venda * (1 - p.desconto_maximo / 100)
        p.desconto = round(p.desconto_maximo)
    return render(request, 'core/ofertas.html', {'produtos': produtos})


def novidades(request):
    return render(request, 'core/novidades.html')

# CATEGORIAS


def masculino(request):
    produtos = Produto.objects.filter(
        ativo=True, categoria__nome__iexact='Masculino'
    )
    for p in produtos:
        if p.desconto_maximo and p.desconto_maximo > 0:
            p.preco_promocional = p.valor_venda * (1 - p.desconto_maximo / 100)
            p.desconto = round(p.desconto_maximo)
        else:
            p.preco_promocional = None
            p.desconto = 0
    return render(request, 'core/categorias/masculino.html', {'produtos': produtos})


def feminino(request):
    produtos = Produto.objects.filter(
        ativo=True, categoria__nome__iexact='Feminino'
    )
    for p in produtos:
        if p.desconto_maximo and p.desconto_maximo > 0:
            p.preco_promocional = p.valor_venda * (1 - p.desconto_maximo / 100)
            p.desconto = round(p.desconto_maximo)
        else:
            p.preco_promocional = None
            p.desconto = 0
    return render(request, 'core/categorias/feminino.html', {'produtos': produtos})


def acessorios(request):
    produtos = Produto.objects.filter(
        ativo=True, categoria__nome__iexact='Acessorios'
    )
    for p in produtos:
        if p.desconto_maximo and p.desconto_maximo > 0:
            p.preco_promocional = p.valor_venda * (1 - p.desconto_maximo / 100)
            p.desconto = round(p.desconto_maximo)
        else:
            p.preco_promocional = None
            p.desconto = 0
    return render(request, 'core/categorias/acessorios.html', {'produtos': produtos})


# -------------------detalhes produto-------------------

def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    preco_promocional = None
    desconto = None

    if produto.desconto_maximo:
        preco_promocional = produto.valor_venda * \
            (1 - produto.desconto_maximo / 100)
        desconto = int(produto.desconto_maximo)

    produtos_similares = Produto.objects.filter(
        categoria=produto.categoria,
        marca=produto.marca,
        ativo=True
    ).exclude(id=produto.id)[:8]

    context = {
        'produto': produto,
        'preco_promocional': preco_promocional,
        'desconto': desconto,
        'produtos_similares': produtos_similares,
    }
    return render(request, 'core/produto_detalhe.html', context)

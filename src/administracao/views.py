from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.forms import modelformset_factory, inlineformset_factory

from .forms import ProdutoForm, VariacaoProdutoForm
from produtos.models import Produto, VariacaoProduto

# Função do painel de administração


def painel_dashboard(request):
    return render(request, 'administracao/dashboard.html')


# Função para o cadastro de produto
def cadastro_produto(request):
    VariacaoFormSet = inlineformset_factory(
        Produto, VariacaoProduto, form=VariacaoProdutoForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        variacoes_formset = VariacaoFormSet(request.POST)
        if form.is_valid() and variacoes_formset.is_valid():
            produto = form.save()
            variacoes = variacoes_formset.save(commit=False)
            for variacao in variacoes:
                variacao.produto = produto
                variacao.save()
            messages.success(
                request, "Produto e variações cadastrados com sucesso.")
            return redirect('administracao:lista_produtos')
        else:
            messages.error(request, "Erro ao cadastrar produto ou variações.")
    else:
        form = ProdutoForm()
        variacoes_formset = VariacaoFormSet()

    return render(request, 'administracao/cad-edita-produtos.html', {
        'form': form,
        'variacoes_formset': variacoes_formset,
    })


# Função para editar produto
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    VariacaoFormSet = inlineformset_factory(
        Produto, VariacaoProduto, form=VariacaoProdutoForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        variacoes_formset = VariacaoFormSet(request.POST, instance=produto)
        if form.is_valid() and variacoes_formset.is_valid():
            form.save()
            variacoes_formset.save()
            messages.success(
                request, "Produto e variações atualizados com sucesso.")
            return redirect('administracao:lista_produtos')
        else:
            messages.error(request, "Erro ao editar produto ou variações.")
    else:
        form = ProdutoForm(instance=produto)
        variacoes_formset = VariacaoFormSet(instance=produto)

    return render(request, 'administracao/cad-edita-produtos.html', {
        'form': form,
        'produto': produto,
        'variacoes_formset': variacoes_formset,
    })


# Função para listar os produtos
def lista_produtos(request):
    busca = request.GET.get('q', '')
    lista = Produto.objects.filter(ativo=True)

    if busca:
        lista = lista.filter(nome__icontains=busca) | lista.filter(
            codigo_interno__icontains=busca)

    paginator = Paginator(lista, 10)
    pagina = request.GET.get('page')
    produtos = paginator.get_page(pagina)

    return render(request, 'administracao/lista_produtos.html', {
        'produtos': produtos,
        'busca': busca
    })


# Função para excluir produto
def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.ativo = False
        produto.save()
        messages.success(request, 'Produto excluído com sucesso.')
        return redirect('administracao:lista_produtos')

    return render(request, 'administracao/excluir_produtos.html', {'produto': produto})

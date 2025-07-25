from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.forms import inlineformset_factory
from django.db.models import Q

from .forms import ProdutoForm, VariacaoProdutoForm, BaseVariacaoProdutoFormSet
from produtos.models import Produto, VariacaoProduto


def painel_dashboard(request):
    return render(request, 'administracao/dashboard.html')


def cadastro_produto(request):
    VariacaoFormSet = inlineformset_factory(
        Produto, VariacaoProduto, form=VariacaoProdutoForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        variacoes_formset = VariacaoFormSet(
            request.POST, request.FILES, instance=None)

        if form.is_valid():
            produto = form.save()
            variacoes_formset = VariacaoFormSet(
                request.POST, request.FILES, instance=produto)
            if variacoes_formset.is_valid():
                variacoes_formset.save()
                messages.success(
                    request, "Produto e variações cadastrados com sucesso.")
                return redirect('administracao:lista_produtos')
            else:
                messages.error(request, "Erro nas variações:")
        else:
            messages.error(request, "Erro no produto:")
        # Se chegou aqui, ou form ou formset inválidos.
        # Garantimos que o formset tem dados para renderizar os erros
        if not form.is_valid():
            # Form inválido, já temos form com erros
            # Já passamos formset acima
            pass
        elif not variacoes_formset.is_valid():
            # Form válido, formset inválido — mantém formset com dados e erros
            pass

    else:
        form = ProdutoForm()
        variacoes_formset = VariacaoFormSet(instance=None)

    return render(request, 'administracao/cad-edita-produtos.html', {
        'form': form,
        'variacoes_formset': variacoes_formset,
    })


def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    VariacaoFormSet = inlineformset_factory(
        Produto, VariacaoProduto, form=VariacaoProdutoForm, formset=BaseVariacaoProdutoFormSet, extra=0, can_delete=True
    )

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        variacoes_formset = VariacaoFormSet(
            request.POST, request.FILES, instance=produto)

        if form.is_valid() and variacoes_formset.is_valid():
            form.save()
            variacoes_formset.save()
            messages.success(
                request, "Produto e variações atualizados com sucesso.")
            return redirect('administracao:lista_produtos')
        else:
            messages.error(request, "Erro ao editar produto ou variações.")
            # Retorna o formulário com erros para o usuário
            return render(request, 'administracao/cad-edita-produtos.html', {
                'form': form,
                'produto': produto,
                'variacoes_formset': variacoes_formset,
            })
    else:
        form = ProdutoForm(instance=produto)
        variacoes_formset = VariacaoFormSet(instance=produto)

    return render(request, 'administracao/cad-edita-produtos.html', {
        'form': form,
        'produto': produto,
        'variacoes_formset': variacoes_formset,
    })


def lista_produtos(request):
    busca = request.GET.get('q', '')
    status = request.GET.get('status', 'ativos')

    produtos = Produto.objects.all()

    # Filtro por status
    if status == 'ativos':
        produtos = produtos.filter(ativo=True)
    elif status == 'inativos':
        produtos = produtos.filter(ativo=False)

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    # Total de estoque somando variações
    total_estoque = sum([
        sum([v.estoque for v in produto.variacoes.all()])
        for produto in produtos
    ])

    # Paginação
    paginator = Paginator(produtos, 10)
    page = request.GET.get('page')
    produtos_paginados = paginator.get_page(page)

    return render(request, 'administracao/lista_produtos.html', {
        'produtos': produtos_paginados,
        'busca': busca,
        'status': status,
        'total_estoque': total_estoque,
    })


def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.ativo = False
        produto.save()
        messages.success(request, 'Produto excluído com sucesso.')
        return redirect('administracao:lista_produtos')

    return render(request, 'administracao/excluir_produtos.html', {'produto': produto})

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.forms import inlineformset_factory
from django.db.models import Q

from .forms import ProdutoForm, VariacaoProdutoForm
from produtos.models import Produto, VariacaoProduto


def painel_dashboard(request):
    return render(request, 'administracao/dashboard.html')


def cadastro_produto(request):
    VariacaoFormSet = inlineformset_factory(
        Produto, VariacaoProduto, form=VariacaoProdutoForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        # Passa None para instance porque produto ainda não existe
        variacoes_formset = VariacaoFormSet(request.POST, instance=None)

        if form.is_valid():
            produto = form.save()
            # Agora que produto existe, criamos o formset com a instância certa
            variacoes_formset = VariacaoFormSet(request.POST, instance=produto)
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
            # mantém form e formset com erros para exibir no template

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
    lista = Produto.objects.all()

    if busca:
        lista = lista.filter(
            Q(nome__icontains=busca) | Q(codigo_interno__icontains=busca)
        )

    paginator = Paginator(lista, 10)
    pagina = request.GET.get('page')
    produtos = paginator.get_page(pagina)

    return render(request, 'administracao/lista_produtos.html', {
        'produtos': produtos,
        'busca': busca
    })


def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.ativo = False
        produto.save()
        messages.success(request, 'Produto excluído com sucesso.')
        return redirect('administracao:lista_produtos')

    return render(request, 'administracao/excluir_produtos.html', {'produto': produto})

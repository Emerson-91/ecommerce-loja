from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.forms import modelformset_factory

from .forms import ProdutoForm, VariacaoProdutoForm, ImagemFormSet
from produtos.models import Produto, VariacaoProduto, ImagemProduto, GradeTamanho


def painel_dashboard(request):
    return render(request, 'administracao/dashboard.html')


def carregar_grades_por_tipo(request):
    tipo = request.GET.get('tipo')
    if tipo == 'all':
        grades = GradeTamanho.objects.all().values('id', 'tamanhos', 'tipo')
    else:
        grades = GradeTamanho.objects.filter(
            tipo=tipo).values('id', 'tamanhos', 'tipo')
    # Adiciona o display do tipo
    grades_list = []
    for g in grades:
        tipo_display = dict(GradeTamanho.TIPOS_GRADE).get(g['tipo'], '')
        g['tipo_display'] = tipo_display
        grades_list.append(g)
    return JsonResponse(grades_list, safe=False)


def cadastro_produto(request):
    produto = None
    grade_tamanhos = []

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)

        if form.is_valid():
            grade = form.cleaned_data.get('grade_tamanho')
            if grade:
                grade_tamanhos = [t.strip() for t in grade.tamanhos.split(',')]

        VariacaoFormSet = modelformset_factory(
            VariacaoProduto,
            form=VariacaoProdutoForm,
            extra=len(grade_tamanhos) or 1,
            can_delete=True
        )

        variacoes_formset = VariacaoFormSet(request.POST, form_kwargs={
                                            'tamanhos_grade': grade_tamanhos})
        imagens_formset = ImagemFormSet(request.POST, request.FILES)

        if form.is_valid() and variacoes_formset.is_valid() and imagens_formset.is_valid():
            produto = form.save()

            for vform in variacoes_formset:
                if vform.cleaned_data and not vform.cleaned_data.get('DELETE'):
                    variacao = vform.save(commit=False)
                    variacao.produto = produto
                    variacao.save()

            for iform in imagens_formset:
                if iform.cleaned_data and not iform.cleaned_data.get('DELETE'):
                    imagem = iform.save(commit=False)
                    imagem.produto = produto
                    imagem.save()

            messages.success(request, "Produto cadastrado com sucesso.")
            return redirect('administracao:lista_produtos')
    else:
        form = ProdutoForm()
        VariacaoFormSet = modelformset_factory(
            VariacaoProduto,
            form=VariacaoProdutoForm,
            extra=1,
            can_delete=True
        )
        variacoes_formset = VariacaoFormSet(
            queryset=VariacaoProduto.objects.none(), form_kwargs={'tamanhos_grade': []})
        imagens_formset = ImagemFormSet(queryset=ImagemProduto.objects.none())

    return render(request, 'administracao/cad-edita-produtos.html', {
        'form': form,
        'produto': produto,
        'variacoes_formset': variacoes_formset,
        'imagens_formset': imagens_formset,
    })


def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    grade = produto.grade_tamanho
    tamanhos_grade = [t.strip()
                      for t in grade.tamanhos.split(',')] if grade else []

    VariacaoFormSet = modelformset_factory(
        VariacaoProduto,
        form=VariacaoProdutoForm,
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        variacoes_formset = VariacaoFormSet(
            request.POST,
            queryset=produto.variacoes.all(),
            form_kwargs={'tamanhos_grade': tamanhos_grade}
        )
        imagens_formset = ImagemFormSet(
            request.POST,
            request.FILES,
            queryset=produto.imagens.all()
        )

        if form.is_valid() and variacoes_formset.is_valid() and imagens_formset.is_valid():
            produto = form.save()

            for variacao_form in variacoes_formset:
                if variacao_form.cleaned_data:
                    if variacao_form.cleaned_data.get('DELETE') and variacao_form.instance.pk:
                        variacao_form.instance.delete()
                    else:
                        v = variacao_form.save(commit=False)
                        v.produto = produto
                        v.save()

            for imagem_form in imagens_formset:
                if imagem_form.cleaned_data:
                    if imagem_form.cleaned_data.get('DELETE') and imagem_form.instance.pk:
                        imagem_form.instance.delete()
                    else:
                        img = imagem_form.save(commit=False)
                        img.produto = produto
                        img.save()

            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('administracao:lista_produtos')
        else:
            messages.error(request, 'Corrija os erros abaixo.')
    else:
        form = ProdutoForm(instance=produto)
        variacoes_formset = VariacaoFormSet(
            queryset=produto.variacoes.all(),
            form_kwargs={'tamanhos_grade': tamanhos_grade}
        )
        imagens_formset = ImagemFormSet(queryset=produto.imagens.all())

    return render(request, 'administracao/cad-edita-produtos.html', {
        'form': form,
        'produto': produto,
        'variacoes_formset': variacoes_formset,
        'imagens_formset': imagens_formset,
    })


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


def excluir_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if request.method == 'POST':
        produto.ativo = False
        produto.save()
        messages.success(request, 'Produto excluído com sucesso.')
        return redirect('administracao:lista_produtos')
    return render(request, 'administracao/excluir_produtos.html', {'produto': produto})

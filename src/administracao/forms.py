from django import forms
from produtos.models import Produto, VariacaoProduto, ImagemProduto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome',
            'codigo_interno',
            'descricao',
            'categoria',
            'marca',
            'grade_tamanho',
            'imagem_principal',
            'valor_venda',
            'peso',
            'altura',
            'largura',
            'ncm',
            'cest',
            'cfop',
            'desconto_maximo',
            'ativo',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_interno': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.Select(attrs={'class': 'form-select'}),
            'grade_tamanho': forms.Select(attrs={'class': 'form-select'}),
            'imagem_principal': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'valor_venda': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control'}),
            'largura': forms.NumberInput(attrs={'class': 'form-control'}),
            'ncm': forms.TextInput(attrs={'class': 'form-control'}),
            'cest': forms.TextInput(attrs={'class': 'form-control'}),
            'cfop': forms.TextInput(attrs={'class': 'form-control'}),
            'desconto_maximo': forms.NumberInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class VariacaoProdutoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        tamanhos_grade = kwargs.pop('tamanhos_grade', [])
        super().__init__(*args, **kwargs)

        self.fields['cor'].widget = forms.TextInput(
            attrs={'class': 'form-control'})
        self.fields['estoque'].widget = forms.NumberInput(
            attrs={'class': 'form-control'})

        if tamanhos_grade:
            self.fields['tamanho'].widget = forms.Select(
                choices=[('', '--- Selecione ---')] + [(t, t)
                                                       for t in tamanhos_grade],
                attrs={'class': 'form-select'}
            )
        else:
            self.fields['tamanho'].widget = forms.TextInput(
                attrs={'class': 'form-control'})

    class Meta:
        model = VariacaoProduto
        fields = ['cor', 'tamanho', 'estoque']


ImagemFormSet = forms.modelformset_factory(
    ImagemProduto,
    fields=('imagem',),
    extra=1,
    can_delete=True,
    widgets={'imagem': forms.ClearableFileInput(
        attrs={'class': 'form-control'})}
)

from django import forms
from produtos.models import Produto, VariacaoProduto, ImagemProduto
import re


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'nome', 'codigo_interno', 'descricao', 'categoria', 'marca',
            'imagem_principal', 'valor_venda', 'peso', 'altura', 'largura',
            'ncm', 'cest', 'cfop', 'desconto_maximo', 'ativo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_interno': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'marca': forms.Select(attrs={'class': 'form-select'}),
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
    class Meta:
        model = VariacaoProduto
        fields = ['cor', 'tamanho', 'estoque']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campo cor como input color com Tailwind
        self.fields['cor'].widget = forms.TextInput(attrs={
            'type': 'color',
            'class': 'w-full h-10 p-0 border border-gray-300 rounded'
        })

        self.fields['tamanho'].widget.attrs.update(
            {'class': 'form-input w-full'})
        self.fields['estoque'].widget.attrs.update(
            {'class': 'form-input w-full'})

    def clean_tamanho(self):
        tamanho = self.cleaned_data['tamanho'].strip().upper()
        if not re.match(r'^[A-Z0-9]+$', tamanho):
            raise forms.ValidationError(
                "Digite apenas letras (A-Z) e números (0-9), sem espaços ou símbolos."
            )
        return tamanho

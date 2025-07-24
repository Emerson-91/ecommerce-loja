from django import forms
from produtos.models import Produto, VariacaoProduto, ImagemProduto

TAMANHO_CHOICES = [
    ('NORMAL', 'Normal'),
    ('PLUS', 'Plus'),
    ('NUMERACAO', 'Numeração'),
]

# Exemplo de tamanhos baseados no tipo
TAMANHOS_NORMAL = ['P', 'M', 'G', 'GG']
TAMANHOS_PLUS = ['P', 'M', 'G', 'GG']
TAMANHOS_NUMERACAO = ['36', '38', '40', '42', '44', '46']


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
    def __init__(self, *args, **kwargs):
        tamanhos_grade = kwargs.pop('tamanhos_grade', [])
        super().__init__(*args, **kwargs)

        # Tipo de tamanho
        self.fields['tipo_tamanho'].widget = forms.Select(
            choices=TAMANHO_CHOICES, attrs={'class': 'form-select w-full'}
        )

        tipo_tamanho = self.data.get('tipo_tamanho', 'NORMAL')
        if tipo_tamanho == 'NORMAL':
            tamanhos = TAMANHOS_NORMAL
        elif tipo_tamanho == 'PLUS':
            tamanhos = TAMANHOS_PLUS
        elif tipo_tamanho == 'NUMERACAO':
            tamanhos = TAMANHOS_NUMERACAO
        else:
            tamanhos = []

        self.fields['tamanho'].widget = forms.Select(
            choices=[('', '--- Selecione ---')] + [(t, t) for t in tamanhos],
            attrs={'class': 'form-select w-full'}
        )

        self.fields['cor'].widget = forms.TextInput(
            attrs={'class': 'form-input w-full'})
        self.fields['estoque'].widget = forms.NumberInput(
            attrs={'class': 'form-input w-full'})

    class Meta:
        model = VariacaoProduto
        fields = ['cor', 'tipo_tamanho', 'tamanho', 'estoque']


# Imagem FormSet
ImagemFormSet = forms.modelformset_factory(
    ImagemProduto,
    fields=('imagem',),
    extra=1,
    can_delete=True,
    widgets={
        'imagem': forms.ClearableFileInput(attrs={'class': 'form-control'})
    }
)

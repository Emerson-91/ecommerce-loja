from django.contrib import admin
from .models import Categoria, Marca, GradeTamanho, Produto, VariacaoProduto, ImagemProduto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'codigo_interno',
                    'valor_venda', 'categoria', 'marca')
    search_fields = ('nome', 'codigo_interno')
    list_filter = ('categoria', 'marca')

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'codigo_interno', 'descricao', 'categoria', 'marca', 'grade_tamanho')
        }),
        ('Preço e Estoque', {
            'fields': ('valor_venda', 'estoque', 'desconto_maximo')
        }),
        ('Dimensões', {
            'fields': ('peso', 'altura', 'largura')
        }),
        ('Informações Fiscais', {
            'fields': ('ncm', 'cest', 'cfop')
        }),
    )


admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(GradeTamanho)
admin.site.register(VariacaoProduto)
admin.site.register(ImagemProduto)

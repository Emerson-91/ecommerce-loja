from django.db import models

# Modelos de Categoria e Marca


class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Marca(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


# Modelos de Produto
class Produto(models.Model):
    nome = models.CharField(max_length=200)
    codigo_interno = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True)

    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    marca = models.ForeignKey(
        Marca, on_delete=models.SET_NULL, null=True, blank=True)

    imagem_principal = models.ImageField(
        upload_to='produtos/', null=True, blank=True)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2)

    peso = models.DecimalField(
        max_digits=6, decimal_places=3, help_text="Em kg", default=0.0)
    altura = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Em cm", default=0.0)
    largura = models.DecimalField(
        max_digits=6, decimal_places=2, help_text="Em cm", default=0.0)

    ncm = models.CharField(max_length=10, blank=True, null=True)
    cest = models.CharField(max_length=10, blank=True, null=True)
    cfop = models.CharField(max_length=10, blank=True, null=True)

    desconto_maximo = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True,
        help_text="Desconto máximo permitido (%)"
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.codigo_interno})"


# Modelos de Variação do Produto
class VariacaoProduto(models.Model):
    TIPO_TAMANHO_CHOICES = [
        ('NORMAL', 'Normal'),
        ('PLUS', 'Plus'),
        ('NUMERACAO', 'Numeração'),
    ]

    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='variacoes')
    cor = models.CharField(max_length=50, blank=True)

    tipo_tamanho = models.CharField(
        max_length=15, choices=TIPO_TAMANHO_CHOICES, default='NORMAL')

    tamanho = models.CharField(max_length=50, blank=True)  # Tamanho do produto
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.produto.nome} - {self.cor} - {self.tipo_tamanho} - {self.tamanho}"


# Imagens adicionais do produto
class ImagemProduto(models.Model):
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='produtos/')

    def __str__(self):
        return f"Imagem de {self.produto.nome}"

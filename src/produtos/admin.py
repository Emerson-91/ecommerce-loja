from django.contrib import admin
from .models import Categoria, Marca


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']

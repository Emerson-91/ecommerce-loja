# src/core/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')


def sobre(request):
    return render(request, 'core/sobre.html')

def contato(request):
    # colocar logica para formulario de contato se necessario
    return render(request, 'core/contato.html')

def politica_privacidade(request):
    return render(request, 'core/politica_privacidade.html')
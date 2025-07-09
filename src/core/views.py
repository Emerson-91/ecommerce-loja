# src/core/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/sobre.html')

def contact(request):
    # colocar logica para formulario de contato se necessario
    return render(request, 'core/contato.html')
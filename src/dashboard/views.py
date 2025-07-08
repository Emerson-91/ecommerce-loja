from django.shortcuts import render
from datetime import datetime

def dashboard_home(request):
    # Contexto para passar dados para o template
    context = {
        'current_date': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    # Renderiza o template 'dashboard/index.html'
    return render(request, 'dashboard/index.html', context)
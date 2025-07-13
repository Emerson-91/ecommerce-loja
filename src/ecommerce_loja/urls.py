from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # 'e do APP Administracao
    path('administracao/', include('administracao.urls')),
    # path('produtos/', include('produtos.urls')),
]

if settings.DEBUG:
    # Servir arquivos estáticos em modo desenvolvimento
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATICFILES_DIRS[0])

    # Servir arquivos de mídia em modo desenvolvimento
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

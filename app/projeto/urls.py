from django.contrib import admin
from django.urls import path, include
from serase_movimentacao.views import StatusServidorView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('status/', StatusServidorView.as_view(), name='status'),
    path('', include('serase_movimentacao.urls')),
    path('', include('serase_login.urls')),
    path('', include('serase_padrao.urls')),
    path('', include('serase_relatorio.urls')),
]

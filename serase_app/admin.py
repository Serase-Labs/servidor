from django.contrib import admin
from .models import Saldo, Categoria, Movimentacao, PadraoMovimentacao

# Register your models here.

admin.site.register(Saldo)
admin.site.register(Categoria)
admin.site.register(Movimentacao)
admin.site.register(PadraoMovimentacao)
admin.site.register(Divida)
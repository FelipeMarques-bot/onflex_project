from django.contrib import admin
from .models import ControleKM, SaidaEstoque, Produto, BaixaEstoque, OrdemServico

# Configuração para exibir melhor as colunas no Admin
class ControleKMAdmin(admin.ModelAdmin):
    list_display = ('tecnico', 'data', 'km_inicial', 'km_final', 'inconsistencia')
    list_filter = ('tecnico', 'inconsistencia')

class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'tecnico', 'data')
    search_fields = ('cliente', 'tecnico__username')

# Registrando tudo
admin.site.register(ControleKM, ControleKMAdmin)
admin.site.register(SaidaEstoque)
admin.site.register(Produto)
admin.site.register(BaixaEstoque)
admin.site.register(OrdemServico, OrdemServicoAdmin)
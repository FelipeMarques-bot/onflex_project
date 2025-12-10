from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    quantidade_estoque = models.IntegerField(default=0)
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nome} (Estoque: {self.quantidade_estoque})"

class ControleKM(models.Model):
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    km_inicial = models.IntegerField()
    km_final = models.IntegerField(null=True, blank=True)
    inconsistencia = models.BooleanField(default=False)
    mensagem_erro = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-data']

    def save(self, *args, **kwargs):
        # REMOVIDA a validação estrita de continuidade de KM a pedido.
        # Agora ele aceita "buracos" na quilometragem sem dar erro.
        super().save(*args, **kwargs)

class SaidaEstoque(models.Model):
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)
    os_servico = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade}"

    def save(self, *args, **kwargs):
        if not self.pk:
            # Permite estoque negativo (apenas registra o uso)
            self.produto.quantidade_estoque -= self.quantidade
            self.produto.save()
        super().save(*args, **kwargs)

class BaixaEstoque(models.Model):
    item = models.CharField(max_length=200, verbose_name="Nome do Item")
    quantidade = models.IntegerField(verbose_name="Quantidade")
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.item} - {self.quantidade}"

class OrdemServico(models.Model):
    tecnico = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=200, verbose_name="Nome do Cliente")
    data = models.DateTimeField(auto_now_add=True)

    # Detalhes do Serviço
    descricao_servico = models.TextField(verbose_name="O que foi feito?")
    pecas_usadas = models.TextField(verbose_name="Peças/Materiais Usados", blank=True, null=True)
    km_percorrida = models.IntegerField(verbose_name="KM Percorrida (Opcional)", blank=True, null=True)

    # Assinatura Digital (Salva como imagem)
    assinatura = models.ImageField(upload_to='assinaturas_os/', blank=True, null=True)

    def __str__(self):
        return f"OS #{self.id} - {self.cliente}"
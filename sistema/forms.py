from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import OrdemServico, BaixaEstoque

class RegistrarTecnicoForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class BaixaEstoqueForm(forms.ModelForm):
    class Meta:
        model = BaixaEstoque
        fields = ['item', 'quantidade']
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Conector RJ45, Cabo...'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Qtd'}),
        }

class OrdemServicoForm(forms.ModelForm):
    # Campo oculto para receber os dados da assinatura (JavaScript vai preencher isso)
    assinatura_base64 = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = OrdemServico
        fields = ['cliente', 'descricao_servico', 'pecas_usadas', 'km_percorrida']
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Cliente / Empresa'}),
            'descricao_servico': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva o serviço realizado...'}),
            'pecas_usadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Liste as peças trocadas (se houver)...'}),
            'km_percorrida': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'KM rodado neste atendimento'}),
        }
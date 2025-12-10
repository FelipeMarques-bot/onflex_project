import uuid
import base64
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders # Importe finders para achar arquivos estáticos
from .models import ControleKM, Produto, SaidaEstoque, OrdemServico
from .forms import RegistrarTecnicoForm, OrdemServicoForm

# --- FUNÇÃO DE SAIR ---
def sair(request):
    logout(request)
    return redirect('login')

def registrar(request):
    if request.method == 'POST':
        form = RegistrarTecnicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada! Faça login.')
            return redirect('login')
    else:
        form = RegistrarTecnicoForm()
    return render(request, 'registration/registrar.html', {'form': form})

@login_required
def dashboard(request):
    ultimo = ControleKM.objects.filter(tecnico=request.user).first()
    km_aberto = True if (ultimo and ultimo.km_final is None) else False
    historico = ControleKM.objects.filter(tecnico=request.user)[:5]
    return render(request, 'dashboard.html', {
        'ultimo': ultimo, 
        'km_aberto': km_aberto, 
        'historico': historico
    })

@login_required
def registrar_km(request):
    if request.method == 'POST':
        try:
            ultimo = ControleKM.objects.filter(tecnico=request.user).first()
            if ultimo and ultimo.km_final is None:
                km_post = request.POST.get('km_final')
                if km_post:
                    km_final = int(km_post)
                    if km_final < ultimo.km_inicial:
                        messages.error(request, "Erro: KM Final menor que Inicial!")
                    else:
                        ultimo.km_final = km_final
                        ultimo.save()
                        messages.success(request, "Dia finalizado!")
                else:
                    messages.error(request, "Informe o KM final.")
            else:
                km_post = request.POST.get('km_inicial')
                if km_post:
                    km_inicial = int(km_post)
                    ControleKM.objects.create(tecnico=request.user, km_inicial=km_inicial)
                    messages.success(request, "Dia iniciado!")
                else:
                    messages.error(request, "Informe o KM inicial.")
        except Exception as e:
            messages.error(request, f"Erro ao registrar KM: {e}")

    return redirect('dashboard')

@login_required
def estoque(request):
    produtos = Produto.objects.all().order_by('nome')

    if request.method == 'POST':
        nome_produto = request.POST.get('produto')
        quantidade = request.POST.get('quantidade')
        os_num = request.POST.get('os')

        try:
            qtd = int(quantidade)
            # Busca ou cria o produto
            produto, created = Produto.objects.get_or_create(
                nome=nome_produto,
                defaults={'quantidade_estoque': 0, 'codigo': str(uuid.uuid4())[:8]}
            )

            # Atualiza estoque (subtrai)
            produto.quantidade_estoque -= qtd
            produto.save()

            # Registra a saída
            SaidaEstoque.objects.create(
                tecnico=request.user,
                produto=produto,
                quantidade=qtd,
                os_referencia=os_num
            )
            messages.success(request, f"Baixa de {qtd}x {nome_produto} realizada!")
        except ValueError:
            messages.error(request, "Erro: Quantidade inválida.")
        except Exception as e:
            messages.error(request, f"Erro ao dar baixa: {e}")

        return redirect('estoque')

    return render(request, 'estoque.html', {'produtos': produtos})

@login_required
def nova_os(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            os_obj = form.save(commit=False)
            os_obj.tecnico = request.user

            assinatura_data = form.cleaned_data.get('assinatura_base64')
            if assinatura_data:
                try:
                    format, imgstr = assinatura_data.split(';base64,') 
                    ext = format.split('/')[-1] 
                    data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                    os_obj.assinatura.save(f"assinatura_os_{request.user.id}.png", data, save=False)
                except:
                    pass 

            os_obj.save()
            return render(request, 'os_sucesso.html', {'os_id': os_obj.id})
    else:
        form = OrdemServicoForm()

    return render(request, 'nova_os.html', {'form': form})

@login_required
def relatorios(request):
    kms = ControleKM.objects.all().order_by('-data')
    saidas = SaidaEstoque.objects.all().order_by('-data')
    ordens = OrdemServico.objects.all().order_by('-data')
    return render(request, 'relatorios.html', {'kms': kms, 'saidas': saidas, 'ordens': ordens})

def eh_admin(user):
    return user.is_staff

@login_required
@user_passes_test(eh_admin)
def area_gestao(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    kms = ControleKM.objects.all().order_by('-data')
    saidas = SaidaEstoque.objects.all().order_by('-data')
    ordens = OrdemServico.objects.all().order_by('-data')

    if data_inicio and data_fim:
        kms = kms.filter(data__date__range=[data_inicio, data_fim])
        saidas = saidas.filter(data__date__range=[data_inicio, data_fim])
        ordens = ordens.filter(data__date__range=[data_inicio, data_fim])

    return render(request, 'admin_dashboard.html', {
        'kms': kms, 'saidas': saidas, 'ordens': ordens,
        'data_inicio': data_inicio, 'data_fim': data_fim
    })

@login_required
@user_passes_test(eh_admin)
def exportar_estoque_pdf(request):
    produtos = Produto.objects.all().order_by('nome')
    template_path = 'relatorio_pdf.html'
    context = {'produtos': produtos}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_estoque.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF')
    return response

# --- FUNÇÃO DE TRADUÇÃO DE CAMINHOS PARA O PDF (AGORA MAIS ROBUSTA) ---
def link_callback(uri, rel):
    """
    Converte URIs locais (como /static/img/logo.png ou /media/assinaturas/...)
    em caminhos de arquivo absolutos para que xhtml2pdf possa encontrá-los.
    """
    # 1. Tenta resolver como arquivo estático (para a logo)
    if uri.startswith(settings.STATIC_URL):
        path = finders.find(uri.replace(settings.STATIC_URL, ''))
        if path:
            return path

    # 2. Tenta resolver como arquivo de mídia (para a assinatura)
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
        if os.path.exists(path):
            return path

    # 3. Se já for um caminho absoluto (como os.assinatura.path retorna), verifica se é seguro
    # Esta é a parte crucial para a assinatura, que vem como caminho absoluto
    if os.path.isabs(uri):
        # Garante que o caminho absoluto esteja dentro do diretório base do projeto
        # para evitar o erro SuspiciousFileOperation
        if uri.startswith(settings.BASE_DIR):
            return uri
        else:
            # Se for um caminho absoluto fora do BASE_DIR, é um erro de segurança
            print(f"Caminho absoluto suspeito fora de BASE_DIR: {uri}")
            return None 

    return uri # Retorna a URI original se não for estático, mídia ou caminho absoluto seguro (ex: URL externa)


@login_required
def baixar_os_pdf(request, os_id):
    os_obj = get_object_or_404(OrdemServico, id=os_id)

    context = {
        'os': os_obj, 
        # 'logo_path' não é mais necessário aqui, o link_callback vai resolver '/static/img/logo.png'
    }

    template_path = 'os_impressao.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="OS_{os_obj.id}.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # Passamos o link_callback para o pisa.CreatePDF
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if pisa_status.err:
        # Se der erro, mostra o HTML para debug
        return HttpResponse('Erro ao gerar PDF. Verifique o HTML: <pre>' + html + '</pre>')
    return response
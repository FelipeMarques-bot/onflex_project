from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from sistema import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('registrar/', views.registrar, name='registrar'),
    path('registrar_km/', views.registrar_km, name='registrar_km'),
    path('estoque/', views.estoque, name='estoque'),
    path('nova_os/', views.nova_os, name='nova_os'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('gestao/', views.area_gestao, name='area_gestao'),
    path('gestao/pdf/', views.exportar_estoque_pdf, name='exportar_estoque_pdf'),
    path('os/pdf/<int:os_id>/', views.baixar_os_pdf, name='baixar_os_pdf'),
    path('sair/', views.sair, name='sair'),
]
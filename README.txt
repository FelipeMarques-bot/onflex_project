# OnFlex BR - Sistema de Gestão de Ordens de Serviço

Este é um sistema web robusto e responsivo, desenvolvido para a OnFlex BR, com o objetivo de otimizar a gestão de operações de campo. Ele centraliza a criação e acompanhamento de Ordens de Serviço (OS), o controle de quilometragem (KM) e a administração do estoque de produtos, tudo isso com foco na eficiência e na digitalização dos processos.

## ✨ Funcionalidades Principais

*   **Geração de Ordens de Serviço (OS) Digitais:** Crie, edite e gerencie OS de forma totalmente digital, com campos para descrição do serviço, peças utilizadas e quilometragem percorrida.
*   **Assinatura Eletrônica:** Colete assinaturas digitais diretamente no dispositivo móvel do técnico, agilizando a aprovação e o fechamento das OS.
*   **Controle de Quilometragem (KM):** Registre e acompanhe a quilometragem percorrida em cada serviço, facilitando o controle de custos e logística.
*   **Gestão de Estoque:** Mantenha um controle preciso do estoque de produtos, com funcionalidades para baixa de materiais e visualização de itens utilizados em relatórios.
*   **Geração de Relatórios em PDF:** Exporte Ordens de Serviço, relatórios de estoque e de quilometragem em formato PDF, prontos para impressão ou arquivamento.
*   **Painel Administrativo Intuitivo:** Uma interface de administração dedicada para gerenciar usuários, produtos, visualizar relatórios e ter uma visão completa das operações.
*   **Design Responsivo:** Acesso e usabilidade otimizados em qualquer dispositivo, seja desktop ou mobile.
*   **Identidade Visual da Empresa:** Cores e logotipo da OnFlex BR integrados ao design do sistema e dos documentos gerados.

## 🚀 Tecnologias Utilizadas

*   **Python:** Linguagem de programação principal.
*   **Django:** Framework web de alto nível para desenvolvimento rápido e seguro.
*   **HTML5, CSS3, JavaScript:** Para a construção da interface do usuário.
*   **Git:** Sistema de controle de versão para gerenciamento do código-fonte.
*   **xhtml2pdf:** Biblioteca para geração de documentos PDF a partir de HTML/CSS.
*   **SQLite:** Banco de dados padrão para desenvolvimento (pode ser configurado para PostgreSQL/MySQL em produção).

⚙️ Como Instalar e Configurar (Para Desenvolvedores)

Para configurar o ambiente de desenvolvimento e rodar o projeto localmente:

1.  Clonar o Repositório:
Para o bloco de código de "Clonar o Repositório", você deve copiar APENAS as duas linhas de comando:
bash git clone https://github.com/FelipeMarques-bot/onflex_project.git cd onflex_project

E no GitHub, você as colocaria assim:
git clone https://github.com/FelipeMarques-bot/onflex_project.git cd onflex_project
git clone https://github.com/FelipeMarques-bot/onflex_project.git
cd onflex_project

2.  Criar e Ativar o Ambiente Virtual:
```bash python3 -m venv venv
source venv/bin/activate ```

3.  Instalar Dependências:
pip install -r requirements.txt
(Nota: Você precisará criar um arquivo `requirements.txt` com todas as bibliotecas que seu projeto utiliza, como `Django`, `xhtml2pdf`, etc. Você pode gerar um com `pip freeze > requirements.txt` no seu ambiente virtual ativado.).

4. Configurar o Banco de Dados:
python manage.py migrate

5. Criar um Superusuário (Admin):
python manage.py createsuperuser

6. Rodar o Servidor de Desenvolvimento:
python manage.py runserver


O sistema estará acessível em `http://127.0.0.1:8000/`.

💡 Como Usar

Acesso de Administrador: Utilize as credenciais do superusuário para acessar o painel administrativo em `/admin` e gerenciar usuários, produtos e visualizar todos os relatórios.
Acesso de Técnicos: Usuários com permissão de técnico podem fazer login para criar novas Ordens de Serviço, registrar quilometragem, dar baixa em materiais e coletar assinaturas.

# Sistema de Agendamento de Preventivas

![Tamanho do Repositório](https://img.shields.io/github/repo-size/tutukkj/Sistema-de-agendamento-de-preventivas?style=for-the-badge) ![Licença](https://img.shields.io/github/license/tutukkj/Sistema-de-agendamento-de-preventivas?style=for-the-badge) ![PHP](https://img.shields.io/badge/PHP-8.0%252B-777BB4?style=for-the-badge&logo=php) ![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.2-7952B3?style=for-the-badge&logo=bootstrap)

Sistema web completo para gestão e agendamento de manutenções preventivas, desenvolvido com foco em usabilidade e eficiência para técnicos e administradores.

## 🎯 Visão do Projeto
Este sistema foi desenvolvido para centralizar e organizar manutenções preventivas, substituindo planilhas dispersas e processos manuais. Técnicos podem visualizar suas agendas, administradores gerenciar todos os agendamentos, e todos acompanham rapidamente o status de cada preventiva.

## ✨ Funcionalidades Principais

### 🔐 Sistema de Autenticação Segura
- Login com verificação de credenciais
- Controle de acesso por níveis de usuário
- Sessões protegidas contra acesso não autorizado

### 📊 Dashboard Intuitivo
- Visão geral dos agendamentos por status
- Estatísticas de preventivas realizadas
- Acesso rápido às funcionalidades principais

### 📅 Gestão de Agendamentos
- Criação de novos agendamentos com dados completos
- Visualização detalhada de cada preventiva
- Edição flexível de agendamentos existentes
- Exclusão com confirmação para evitar erros

### 🔍 Filtros e Buscas
- Busca por equipamento, técnico ou data
- Filtros por status (agendado, em andamento, concluído)
- Visualização por período personalizado

### 📱 Design Responsivo
- Interface adaptada para desktop, tablet e mobile
- Navegação otimizada para dispositivos touch
- Layout ajustável a diferentes tamanhos de tela

## 🛠️ Tecnologias Implementadas

**Backend**
- PHP 8.0+ - Lógica de negócio e processamento
- MySQL 8.0 - Banco de dados relacional
- PDO - Conexão segura com o banco de dados
- Sessions - Controle de autenticação e permissões

**Frontend**
- HTML5 - Estrutura semântica das páginas
- CSS3 - Estilização avançada e responsiva
- Bootstrap 5.2 - Framework CSS para layout responsivo
- JavaScript - Interatividade e validações
- Font Awesome - Ícones para melhor experiência visual

**Segurança**
- Prevenção contra SQL Injection (prepared statements)
- Validação de dados no frontend e backend
- Proteção contra XSS (sanitização de entradas)
- Controle de sessões com tempo de expiração

## 📦 Instalação e Configuração

### Pré-requisitos
- Servidor web (Apache/Nginx)
- PHP 8.0 ou superior
- MySQL 8.0 ou superior
- Git (para clonar o repositório)

### Passo a Passo
1. Clone o repositório:
```bash
git clone https://github.com/tutukkj/Sistema-de-agendamento-de-preventivas.git
cd Sistema-de-agendamento-de-preventivas
```
2. Configure o servidor web:
   - Document root apontando para a pasta do projeto
   - Certifique-se de que o `mod_rewrite` está habilitado

3. Configure o banco de dados:
```sql
CREATE DATABASE preventivas_db;
CREATE USER 'preventivas_user'@'localhost' IDENTIFIED BY 'senha_segura';
GRANT ALL PRIVILEGES ON preventivas_db.* TO 'preventivas_user'@'localhost';
FLUSH PRIVILEGES;
```
4. Importe a estrutura do banco:
   - Execute o arquivo `database/schema.sql` no MySQL
   - Ou importe via phpMyAdmin

5. Configure as variáveis de ambiente em `config/database.php`:
```php
define('DB_HOST', 'localhost');
define('DB_NAME', 'preventivas_db');
define('DB_USER', 'preventivas_user');
define('DB_PASS', 'senha_segura');
```
6. Acesse a aplicação:
   - Abra `http://localhost/caminho_do_projeto`
   - Credenciais padrão: `admin / admin123` (alterar após o primeiro login)

## 🚀 Como Utilizar o Sistema

### Para Administradores
- Login com credenciais administrativas
- Dashboard com visão geral do sistema
- Gerenciar usuários e agendamentos
- Criar novos agendamentos com todos os detalhes

### Para Técnicos
- Login com credenciais pessoais
- Visualizar agenda pessoal
- Atualizar status das preventivas
- Registrar observações sobre cada serviço

### Fluxo de um Agendamento
1. Criação - Administrador cria o agendamento
2. Atribuição - Define técnico e data
3. Execução - Técnico atualiza status para "em andamento"
4. Conclusão - Técnico marca como concluído e adiciona observações
5. Histórico - Disponível para consultas futuras

## 📁 Estrutura do Projeto
```
Sistema-de-agendamento-de-preventivas/
├── assets/                 # Arquivos estáticos
│   ├── css/               # Folhas de estilo
│   ├── js/                # Scripts JavaScript
│   └── images/            # Imagens e ícones
├── includes/              # Arquivos de inclusão
│   ├── config/            # Configurações do sistema
│   ├── database/          # Conexão e queries
│   ├── auth/              # Autenticação e sessões
│   └── functions/         # Funções utilitárias
├── pages/                 # Páginas do sistema
│   ├── admin/             # Painel administrativo
│   ├── agendamentos/      # Gestão de agendamentos
│   ├── auth/              # Autenticação
│   └── dashboard/         # Dashboard principal
├── database/              # Scripts do banco de dados
│   └── schema.sql         # Estrutura do banco
└── README.md              # Documentação
```

## 🔧 Personalização e Extensões
- Adicionar novos campos aos agendamentos
- Criar novos relatórios em `pages/admin/`
- Integrar com outros sistemas via API REST ou Webhooks
- Implementar exportação para PDF, Excel ou CSV




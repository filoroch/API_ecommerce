# Alterações no Projeto API E-commerce

## Migração para Arquitetura MVC

### Estrutura de Pastas
- Criação da estrutura de pastas MVC (`models`, `views`, `controllers`)
- Separação clara de responsabilidades entre as camadas

### Reorganização de Arquivos
- **Models**: Todas as definições de banco de dados (User, Product) foram movidas para `models.py`
- **Controllers**: Lógica de negócios separada em:
  - `controllers/auth_controller.py`: gerencia autenticação (register, login, logout)
  - `controllers/product_controller.py`: operações CRUD para produtos
- **Views**: Rotas e Blueprint management em `views/routes.py`
- **Inicialização**: Arquivos `__init__.py` adicionados para marcar diretórios como pacotes Python

### Correções e Melhorias
- Resolução de problemas de importação circular entre módulos
- Configuração do SQLAlchemy para inicialização com `init_app()`
- Implementação de Blueprints para melhor organização e modularidade
- Adição de rota de boas-vindas na raiz da aplicação

## Integração com Swagger UI
- Adição da biblioteca `flasgger` para documentação da API
- Configuração do Swagger UI apontando para `swagger.yaml` existente
- Exposição de endpoint `/swagger/` para visualização da documentação interativa

## Execução em Ambientes Diversos
- Criação do arquivo `run.py` para facilitar execução em diferentes ambientes
- Configuração de host `0.0.0.0` para permitir acesso de qualquer IP
- Suporte a execução em ambientes cloud como GitHub Codespaces

## Dependências Adicionadas
- `flasgger`: Para integração do Swagger UI na aplicação Flask

## Benefícios da Nova Estrutura
- **Manutenibilidade**: Código mais organizado e fácil de manter
- **Escalabilidade**: Facilidade para adicionar novos módulos e funcionalidades
- **Testabilidade**: Separação de responsabilidades facilita testes unitários
- **Documentação**: API totalmente documentada e interativa com Swagger UI

Estas alterações proporcionam maior escalabilidade, manutenibilidade e documentação adequada ao projeto, seguindo as melhores práticas de desenvolvimento com Flask.
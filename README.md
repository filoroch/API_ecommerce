# API E-commerce

Uma API RESTful para sistema de e-commerce construída com Flask, implementando o padrão de arquitetura MVC (Model-View-Controller) e documentada com Swagger UI.

## Estrutura do Projeto

```
├── app.py               # Arquivo principal da aplicação Flask e configurações
├── models.py            # Definições dos modelos SQLAlchemy (User, Product)
├── controllers/         # Lógica de controle para as entidades
│   ├── auth_controller.py   # Controle de autenticação (login, registro)
│   └── product_controller.py # Operações CRUD para produtos
├── views/               # Definições das rotas HTTP da API
│   └── routes.py        # Configuração de blueprints e rotas
├── run.py               # Script para execução da aplicação
├── swagger.yaml         # Documentação da API para Swagger
├── requirements.txt     # Dependências do projeto
└── instance/            # Dados persistentes (banco SQLite)
    └── ecommerce.db     # Banco de dados SQLite
```

## Tecnologias Utilizadas

- **Flask**: Framework web em Python
- **SQLAlchemy**: ORM para interação com o banco de dados
- **Flask-Login**: Gerenciamento de autenticação
- **Flask-CORS**: Suporte a Cross-Origin Resource Sharing
- **Flasgger**: Integração Swagger para documentação interativa

## Requisitos

- Python 3.6+
- Bibliotecas especificadas em `requirements.txt`

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/filoroch/API_ecommerce.git
   cd API_ecommerce
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Como Executar

Execute o seguinte comando para iniciar a aplicação:

```bash
python run.py
```

A API estará disponível em `http://localhost:5000`
A documentação Swagger estará em `http://localhost:5000/swagger/`

## Endpoints da API

### Autenticação

- **POST /register**: Registra um novo usuário
  ```json
  {
    "username": "usuario",
    "password": "senha123"
  }
  ```

- **POST /login**: Realiza login
  ```json
  {
    "username": "usuario",
    "password": "senha123"
  }
  ```

- **POST /logout**: Realiza logout (requer autenticação)

### Produtos

- **GET /api/products**: Lista todos os produtos
- **POST /api/products/add**: Adiciona um novo produto (requer autenticação)
  ```json
  {
    "name": "Produto Exemplo",
    "price": 99.99,
    "description": "Descrição do produto"
  }
  ```
- **DELETE /api/products/delete/{product_id}**: Remove um produto (requer autenticação)

## Documentação Interativa

A documentação completa da API está disponível através do Swagger UI, acessível pelo endpoint `/swagger/` quando a aplicação está em execução.

![Swagger UI Screenshot](https://example.com/swagger-screenshot.png)

## Desenvolvimento

O projeto segue o padrão de arquitetura MVC:

- **Models**: Definição das estruturas de dados e lógica de negócios
- **Views**: Rotas HTTP e serialização de dados
- **Controllers**: Lógica de controle entre Models e Views

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das alterações (`git commit -am 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

# Atividade criar API com Flask

Este projeto apresenta uma API simples, capaz de executar as operações básicas do CRUD, em **Flask**, 
além de um front simples capaz de consumir os recursos oferecidos pela API. 
Tem como objetivo exercitar os conceitos vistos em sala de aula sobre o desenvolvimento de APIs.

## Funcionalidades

- **Criar um livro**: Permite adicionar um novo livro à biblioteca.
- **Listar todos os livros**: Exibe todos os livros cadastrados na biblioteca.
- **Atualizar um livro**: Permite editar as informações de um livro existente.
- **Deletar livros**: Permite excluir livros da biblioteca.

## Tecnologias Utilizadas

- **Back-end**: 
  - Flask (Python)
  - SQLite (Banco de dados)
- **Front-end**: 
  - HTML
  - JavaScript (Vanilla)

## Instalação e Execução

### Pré-requisitos

1. **Python 3.x** instalado em sua máquina.
2. **Pip** para instalar pacotes do Python.

### Passos para rodar a API

1. Clone este repositório:

    ```bash
    git clone https://github.com/alysonGuimaraes/Atividade-API-Flask.git
    cd Atividade-API-Flask
    ```

2. Instale as dependências necessárias:

    ```bash
    pip install flask
    pip install flask_sqlalchemy
    pip install flask_cors
    pip install flasgger
    ```

3. Execute o servidor Flask:

    ```bash
    python app.py
    ```

4. A API estará disponível em `http://127.0.0.1:5000/`.

### Para rodar o Front-end:

1. Abra o arquivo `index.html` com o **Live Server** no seu editor de código (como o Visual Studio Code) ou em qualquer outro servidor local.
2. A interface estará acessível no navegador e conectará automaticamente à API para consumo dos dados.

## Endpoints da API

- **GET /book**: Retorna todos os livros cadastrados.
- **GET /book/{id}**: Retorna um livro específico pelo seu ID.
- **POST /book**: Cria um novo livro.
- **PUT /book/{id}**: Atualiza um livro existente pelo ID.
- **DELETE /book/{id}**: Deleta um livro existente pelo ID.

## Exemplo de Requisição

### Criar um livro (POST)

```json
{
  "name": "1984",
  "author": "George Orwell",
  "genre": "Distopia",
  "num_pages": 328,
  "des_synopsis": "Uma distopia sobre vigilância.",
  "flg_completed": true
} 
```

### Resposta de sucesso
```json
{
    "book": {
        "author": "William Gibson",
        "des_observacao": null,
        "des_synopsis": "Um hacker é contratado para realizar um ataque virtual em um mundo cyberpunk.",
        "flg_completed": false,
        "genre": "Ficção Científica",
        "id": 5,
        "name": "Neuromancer",
        "num_pages": 271
    },
    "message": "Book created",
    "status": "success"
}
```

## Documentação com Swagger

- Após a execução do back é possível acessar a documentação pelo endpoint raiz da aplicação:
```http://localhost:5000/``` ou ```http://127.0.0.1:5000/```



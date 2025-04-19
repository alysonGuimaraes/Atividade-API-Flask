from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataBase.db'
db = SQLAlchemy(app)

CORS(app, origins=['http://127.0.0.1:5500'])


app.config['SWAGGER'] = {
    'title': 'booksAPI',
    'description': 'API construída com Flask que permite cadastrar, listar, atualizar e remover livros.',
    'version': '1.0.0',
    'route': '/'
}

Swagger(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    genre = db.Column(db.String(10), nullable=False)
    num_pages = db.Column(db.Integer(), nullable=False)
    des_synopsis = db.Column(db.String(100), nullable=True)
    flg_completed = db.Column(db.Boolean, nullable=False, default=False)
    des_observacao = db.Column(db.String(50), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'genre': self.genre,
            'num_pages': self.num_pages,
            'des_synopsis': self.des_synopsis,
            'flg_completed': self.flg_completed,
            'des_observacao': self.des_observacao
        }


with app.app_context():
    db.create_all()

#Endpoint para obter todos os livros
@app.route("/book", methods=['GET'])
def get_all_books():
    """
    Retorna todos os livros cadastrados
    ---
    tags:
      - Book
    responses:
      200:
        description: Lista de livros
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "1984"
              author:
                type: string
                example: "George Orwell"
              genre:
                type: string
                example: "Distopia"
              num_pages:
                type: integer
                example: 328
              des_synopsis:
                type: string
                example: "Uma distopia sobre vigilância."
              flg_completed:
                type: boolean
                example: true
    """
    books = Book.query.all()
    return jsonify({
        "status": "success",
        "books": [book.serialize() for book in books]
    }), 200

#Endpoint para obter livro pelo id
@app.route("/book/<int:book_id>", methods=['GET'])
def get_book(book_id):
    """
            Obter livro pelo id
            ---
            tags:
              - Book
            parameters:
              - in: path
                name: book_id
                required: true
                type: integer
                description: Id do livro a ser buscado
            responses:
              200:
                description: Livro encontrado com sucesso
                schema:
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: "1984"
                    author:
                      type: string
                      example: "George Orwell"
                    genre:
                      type: string
                      example: "Distopia"
                    num_pages:
                      type: integer
                      example: 328
                    des_synopsis:
                      type: string
                      example: "Uma distopia sobre vigilância."
                    flg_completed:
                      type: boolean
                      example: true
              400:
                description: Dados inválidos
            """
    book = Book.query.filter_by(id=book_id).first()
    # print(book)
    if book is None:
        return jsonify({"status": "error", 'message': 'Book not found'}), 404
    return jsonify({
        "status": "success",
        "book": book.serialize()
    }), 200


#Endpoint de cadastro de livro
@app.route("/book", methods=['POST'])
def register_book():
    """
        Cadastra um novo livro
        ---
        tags:
          - Book
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: book_json
              required:
                - name
                - author
                - genre
                - num_pages
              properties:
                name:
                  type: string
                  example: "1984"
                author:
                  type: string
                  example: "George Orwell"
                genre:
                  type: string
                  example: "Distopia"
                num_pages:
                  type: integer
                  example: 328
                des_synopsis:
                  type: string
                  example: "Uma distopia sobre vigilância governamental."
                flg_completed:
                  type: boolean
                  example: true
        responses:
          201:
            description: Livro criado com sucesso
          400:
            description: Dados inválidos
        """
    # Obtem e separa os dados enviados na requisição
    book_data = request.get_json()
    name = book_data['name']
    author = book_data['author']
    genre = book_data['genre']
    num_pages = book_data['num_pages']
    des_synopsis = book_data['des_synopsis']
    des_observacao = book_data['des_observacao']
    flg_completed = book_data['flg_completed']

    # Trecho usado para verificar se um objeto
    book_exists = Book.query.filter_by(name=name, author=author).first()
    if book_exists:
        return jsonify({'status': 'error', 'message': 'Book already exists'}), 409
    new_book = Book(name=name, author=author, genre=genre, num_pages=num_pages, des_synopsis=des_synopsis, flg_completed=flg_completed, des_observacao=des_observacao)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Book created",
        "book": new_book.serialize()
    }), 201

#Endpoint para atualizar o cadastro do livro pelo id
@app.route('/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
        Atualiza completamente um livro pelo ID
        ---
        tags:
          - Book
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: ID do livro a ser atualizado
          - name: body
            in: body
            required: true
            schema:
              type: object
              required:
                - name
                - author
                - genre
                - num_pages
                - des_synopsis
                - flg_completed
              properties:
                name:
                  type: string
                  example: "Dom Casmurro"
                author:
                  type: string
                  example: "Machado de Assis"
                genre:
                  type: string
                  example: "Romance"
                num_pages:
                  type: integer
                  example: 256
                des_synopsis:
                  type: string
                  example: "Uma história clássica sobre ciúmes e dúvida."
                flg_completed:
                  type: boolean
                  example: true
        responses:
          200:
            description: Livro atualizado com sucesso
            schema:
                properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: "1984"
                    author:
                      type: string
                      example: "George Orwell"
                    genre:
                      type: string
                      example: "Distopia"
                    num_pages:
                      type: integer
                      example: 328
                    des_synopsis:
                      type: string
                      example: "Uma distopia sobre vigilância."
                    flg_completed:
                      type: boolean
                      example: true
          404:
            description: Livro não encontrado
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Book not found
        """
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({"status": "error", "message": "Book not found"}), 404

    new_data = request.get_json()
    book.name = new_data['name']
    book.author = new_data['author']
    book.genre = new_data['genre']
    book.num_pages = new_data['num_pages']
    book.des_synopsis = new_data['des_synopsis']
    book.des_observacao = new_data['des_observacao']
    book.flg_completed = new_data['flg_completed']

    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Book updated",
        "book": book.serialize()
    }), 200


# Endpoint para deletar livro pelo id
@app.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
        Deleta um livro pelo ID
        ---
        tags:
          - Book
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: ID do livro a ser deletado
        responses:
          200:
            description: Livro deletado com sucesso
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: success
                message:
                  type: string
                  example: Book deleted
          404:
            description: Livro não encontrado
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: Book not found
        """
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({"status": "error", "message": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"status": "success", "message": "Book deleted"}), 200


@app.route('/')
def index():
    return redirect('/apidocs')


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataBase.db'
db = SQLAlchemy(app)

CORS(app, origins=['http://127.0.0.1:5500'])


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
    books = Book.query.all()
    return jsonify([book.serialize() for book in books])

#Endpoint para obter livro pelo id
@app.route("/book/<int:book_id>", methods=['GET'])
def get_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    # print(book)
    if book is None:
        return jsonify({"status": "error", 'message': 'Book not found'}), 404
    return jsonify(book.serialize())


#Endpoint de cadastro de livro
@app.route("/book", methods=['POST'])
def register_book():
    # Obtem e separa os dados enviados na requisição
    book_data = request.get_json()
    name = book_data['name']
    author = book_data['author']
    genre = book_data['genre']
    num_pages = book_data['num_pages']
    des_synopsis = book_data['des_synopsis']

    # Trecho usado para verificar se um objeto
    book_exists = Book.query.filter_by(name=name, author=author).first()
    if book_exists:
        return jsonify({'status': 'error', 'message': 'Book already exists'}), 409
    new_book = Book(name=name, author=author, genre=genre, num_pages=num_pages, des_synopsis=des_synopsis)
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.serialize()), 201

#Endpoint para atualizar o cadastro do livro pelo id
@app.route('/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
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

    db.session.commit()
    return jsonify({
        "status": "success",
        "message": "Book updated",
        "book": book.serialize()
    }), 200


# Endpoint para deletar livro cadastrado pelo id
@app.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({"status": "error", "message": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"status": "success", "message": "Book deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# ---------------- Initialize Flask App ----------------
app = Flask(__name__)

# ---------------- Configure Database ----------------
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3306/book_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ---------------- Book Model ----------------
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isRead = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=True)
    language = db.Column(db.String(50), nullable=True)

    def __init__(self, title, author, isRead=False, price=None, language=None):
        self.title = title
        self.author = author
        self.isRead = isRead
        self.price = price
        self.language = language

# ---------------- Create Tables ----------------
with app.app_context():
    db.create_all()

# ---------------- CRUD Routes ----------------

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    return jsonify({
        'books': [
            {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'isRead': book.isRead,
                'price': book.price,
                'language': book.language
            } for book in all_books
        ]
    })

# Get a single book by ID
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isRead': book.isRead,
        'price': book.price,
        'language': book.language
    })

# Add a new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isRead = data.get('isRead', False)
    price = data.get('price')
    language = data.get('language')

    if not title or not author:
        return jsonify({'error': 'Title and author are required'}), 400

    if Book.query.filter_by(title=title).first():
        return jsonify({'error': 'Book with this title already exists'}), 409

    new_book = Book(title, author, isRead, price, language)
    db.session.add(new_book)
    db.session.commit()
    return jsonify({
        'id': new_book.id,
        'title': new_book.title,
        'author': new_book.author,
        'isRead': new_book.isRead,
        'price': new_book.price,
        'language': new_book.language
    }), 201

# Update a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    isRead = data.get('isRead')
    price = data.get('price')
    language = data.get('language')

    if title:
        book.title = title
    if author:
        book.author = author
    if isRead is not None:
        book.isRead = isRead
    if price is not None:
        book.price = price
    if language:
        book.language = language

    db.session.commit()
    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isRead': book.isRead,
        'price': book.price,
        'language': book.language
    })

# Delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

# ---------------- Run the App ----------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)

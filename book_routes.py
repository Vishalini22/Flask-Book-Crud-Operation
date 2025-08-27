from flask import Blueprint, request, jsonify

book_bp = Blueprint("books", __name__)

# Import models and controller inside functions to avoid circular imports
@book_bp.route("/", methods=["GET"])
def get_books():
    from controllers import book_controller
    books = book_controller.get_all_books()
    return jsonify([
        {"id": b.id, "title": b.title, "author": b.author, "isRead": b.isRead,
         "price": b.price, "language": b.language} for b in books
    ])

@book_bp.route("/<int:id>", methods=["GET"])
def get_book(id):
    from controllers import book_controller
    book = book_controller.get_book_by_id(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"id": book.id, "title": book.title, "author": book.author,
                    "isRead": book.isRead, "price": book.price, "language": book.language})

@book_bp.route("/", methods=["POST"])
def add_book():
    from controllers import book_controller
    from models.book import Book
    from app import db

    data = request.get_json()
    if not data.get("title") or not data.get("author"):
        return jsonify({"error": "Title and Author required"}), 400
    if Book.query.filter_by(title=data['title']).first():
        return jsonify({"error": "Book with this title already exists"}), 409
    book = book_controller.create_book(data)
    return jsonify({"id": book.id, "title": book.title, "author": book.author,
                    "isRead": book.isRead, "price": book.price, "language": book.language}), 201

@book_bp.route("/<int:id>", methods=["PUT"])
def update_book_route(id):
    from controllers import book_controller
    book = book_controller.get_book_by_id(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    data = request.get_json()
    book = book_controller.update_book(book, data)
    return jsonify({"id": book.id, "title": book.title, "author": book.author,
                    "isRead": book.isRead, "price": book.price, "language": book.language})

@book_bp.route("/<int:id>", methods=["DELETE"])
def delete_book_route(id):
    from controllers import book_controller
    book = book_controller.get_book_by_id(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    book_controller.delete_book(book)
    return jsonify({"message": "Book deleted successfully"})

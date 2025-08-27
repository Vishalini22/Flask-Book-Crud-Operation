from extensions import db
from models.book import Book

def get_all_books():
    return Book.query.all()

def get_book_by_id(id):
    return Book.query.get(id)

def create_book(data):
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return book

def update_book(book, data):
    for key, value in data.items():
        setattr(book, key, value)
    db.session.commit()
    return book

def delete_book(book):
    db.session.delete(book)
    db.session.commit()

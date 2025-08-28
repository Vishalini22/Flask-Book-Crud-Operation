from extensions import db

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    isRead = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=True)
    language = db.Column(db.String(50), nullable=True)

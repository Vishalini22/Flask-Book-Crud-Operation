from flask import Flask
from extensions import db
from routes.book_routes import book_bp

app = Flask(__name__)

# MySQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/library_db_mysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db
db.init_app(app)

# Register blueprint
app.register_blueprint(book_bp, url_prefix="/books")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This will create tables in MySQL if they don't exist
    app.run(debug=True)

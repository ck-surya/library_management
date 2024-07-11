from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database URI
DB_URI = os.getenv("DB_URI")

# Use the DB_URI in your application configuration

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    published_date = db.Column(db.Date)
    isbn = db.Column(db.String(13))
    pages = db.Column(db.Integer)
    available = db.Column(db.Boolean, default=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    issue_date = db.Column(db.Date, default=datetime.utcnow)
    return_date = db.Column(db.Date)

@app.route('/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        data = request.get_json()
        new_book = Book(
            title=data['title'],
            author=data['author'],
            published_date=data.get('published_date'),
            isbn=data.get('isbn'),
            pages=data.get('pages')
        )
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Book added!'}), 201

    books = Book.query.all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'published_date': book.published_date,
        'isbn': book.isbn,
        'pages': book.pages,
        'available': book.available
    } for book in books])

@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_book(id):
    book = Book.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'published_date': book.published_date,
            'isbn': book.isbn,
            'pages': book.pages,
            'available': book.available
        })

    if request.method == 'PUT':
        data = request.get_json()
        book.title = data['title']
        book.author = data['author']
        book.published_date = data.get('published_date')
        book.isbn = data.get('isbn')
        book.pages = data.get('pages')
        book.available = data.get('available')
        db.session.commit()
        return jsonify({'message': 'Book updated!'})

    if request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted!'})
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=data['password']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added!'}), 201

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'email': user.email
    } for user in users])

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email
    })

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.name = data['name']
    user.email = data['email']
    user.password = data['password']
    db.session.commit()
    return jsonify({'message': 'User updated!'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted!'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

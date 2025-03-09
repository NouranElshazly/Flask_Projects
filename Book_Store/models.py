from database import db
class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    books = db.relationship('Book', backref='author', lazy=True)
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(255), nullable=True)   
    description = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    publish_date = db.Column(db.Date, nullable=False)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    price = db.Column(db.Float, nullable=False)
    appropriate = db.Column(db.String(20), nullable=False)


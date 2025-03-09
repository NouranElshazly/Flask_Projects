from flask import  Flask ,render_template, request ,redirect ,url_for
 
from flask_bootstrap import Bootstrap
from database import db
from models import Book,Author

from forms.register import AuthorForm, RegisterForm
app = Flask(__name__)  #name = import of the exit file == "app"
Bootstrap(app)
#WTF_CONF
app.config['SECRET_KEY'] = 'b9c80b7d2ab1b56afd5996e677f60644'
#DB_CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
#home page

#add books
@app.route('/addbooks' , endpoint="add_books" , methods=['GET' , 'POST'])
def register():
    form = RegisterForm() #book from 
    authors = Author.query.all()
    if not authors :
        return redirect(url_for('add_author'))
    form.author_id.choices = [
         (author.id , author.name)
         for author in authors 
    ]
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            image = form.image.data,
            description = form.description.data,
            publish_date=form.publish_date.data,
            price=form.price.data,
            appropriate=form.appropriateness.data,
            author_id=form.author_id.data
        )
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html' ,form = form)
@app.route('/add_author',methods=['GET' , 'POST'])
def add_author():
    form = AuthorForm()
    if form.validate_on_submit():
        author = Author( name = form.Name.data)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('author_details' ,id=author.id  ))
    return render_template('add_author.html', form = form)
@app.route('/authors')
def all_authors():
     authors = Author.query.all()
     return render_template('authors.html', authors= authors )
@app.route('/author_details/<int:id>' , endpoint="author_details" ,methods=['GET' ])
def author_details(id):
        author = Author.query.get(id)
        if author :
             
             return render_template('author_details.html' , author = author  )
        return render_template ("404.html"), 404
     
   
@app.route('/book')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)

#confirm added
@app.route('/success' , endpoint='success')
def success():
    return render_template('success.html')
#book details
@app.route('/book/<int:id>',endpoint='book_detail' , methods=["GET"] )
def book_detail(id):
        book = Book.query.get(id)
        if book:
             author = book.author
             return render_template('book_details.html', book=book , author=author)
        return render_template ("404.html"), 404
    
#error handler
@app.errorhandler(404)
def page_not_found(e):
    return render_template ('404.html')
@app.errorhandler(500)
def page_not_found(e):
    return render_template ('500.html')
if __name__ == "__main__":
        with app.app_context():
            db.create_all()
            app.run(debug=True)


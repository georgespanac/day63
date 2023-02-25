from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import Label, SubmitField, StringField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "some secret string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////books-collection.db'
db = SQLAlchemy(app)


class BookDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


class Book:
    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating

class AddBookForm(FlaskForm):
    book_name_label = Label(field_id="book_name", text="Book Name")
    book_name = StringField(label='book_name')
    book_author_label = Label(field_id="book_author", text="Book Author")
    book_author = StringField(label='book_author')
    book_rating_label = Label(field_id="book_rating", text="Book Rating")
    book_rating = StringField(label='book_rating')
    add_book_button = SubmitField("Add Book")


class EditRatingForm(FlaskForm):
    book_name_label = Label(field_id="book_name", text="Book Name")
    current_rating_label = Label(field_id="book_name", text="Current rating")
    new_rating = StringField(label='new_rating')
    change_rating_button = SubmitField("Change Rating")

@app.route('/')
def home():
    all_books = db.session.query(BookDB).all()
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    add_book = AddBookForm()
    if add_book.validate_on_submit():
        db.create_all()
        new_book = BookDB(title=add_book.book_name.data, author=add_book.book_author.data,
                        rating=float(add_book.book_rating.data))
        db.session.add(new_book)
        db.session.commit()
        all_books = db.session.query(BookDB).all()
        return render_template('index.html', all_books=all_books)
    else:
        return render_template('add.html', form=add_book)


@app.route("/edit_rating/<book_id>", methods=["GET", "POST"])
def edit_rating(book_id):
    form = EditRatingForm()
    book = BookDB.query.get(book_id)
    if form.validate_on_submit():
        new_rating = form.new_rating.data
        book_to_update = BookDB.query.get(book_id)
        book_to_update.rating = new_rating
        db.session.commit()
        all_books = db.session.query(BookDB).all()
        return render_template('index.html', all_books=all_books)
    else:
        return render_template('edit_rating.html', form=form, book=book)


    print(book_id)

if __name__ == "__main__":
    app.run(debug=True)


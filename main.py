from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import Label, SubmitField, StringField

app = Flask(__name__)
app.secret_key = "some secret string"

all_books = []

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

@app.route('/')
def home():
    return render_template('index.html', all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    add_book = AddBookForm()
    if add_book.validate_on_submit():
        b = Book(title=add_book.book_name.data, author=add_book.book_author.data,
                 rating=add_book.book_rating.data)
        all_books.insert(0, b)
        return render_template('index.html', all_books=all_books)
    else:
        return render_template('add.html', form=add_book)

if __name__ == "__main__":
    app.run(debug=True)


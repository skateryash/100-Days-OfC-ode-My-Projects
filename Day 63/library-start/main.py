from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# all_books = []
app.app_context().push()

# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f"{self.title} - {self.author} - {self.rating}/10 "


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # CREATE RECORD
        new_book = Book(title=request.form.get("book_name"),
                        author=request.form.get("author"),
                        rating=request.form.get("rating"))
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        # UPDATE RECORD
        book_id = request.form.get("id")
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form.get("rating")
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get("id")
    book_selected = Book.query.get(book_id)
    return render_template('edit.html', book=book_selected)


@app.route('/delete')
def delete():
    book_id = request.args.get("id")
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)


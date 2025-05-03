from flask import Flask, render_template, request, redirect, url_for, flash, g
from db import get_db, close_db
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Register database connection handler for teardown
app.teardown_appcontext(close_db)

# Create a before_request handler that doesn't return anything
@app.before_request
def before_request():
    get_db()

@app.route('/')
def index():
    # Get the database and books collection
    db = g.db
    books = list(db.books.find())
    return render_template('index.html', books=books)

@app.route('/view/<book_id>')
def view(book_id):
    # Get the specific book
    db = g.db
    book = db.books.find_one({'_id': ObjectId(book_id)})
    return render_template('view.html', book=book)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Add new book
        db = g.db
        new_book = {
            'title': request.form['title'],
            'author': request.form['author'],
            'year': int(request.form['year']),
            'genre': request.form['genre'],
            'read': 'read' in request.form
        }
        
        db.books.insert_one(new_book)
        flash('Book added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('report-item.html')

@app.route('/delete/<book_id>')
def delete(book_id):
    # Delete a book
    db = g.db
    db.books.delete_one({'_id': ObjectId(book_id)})
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
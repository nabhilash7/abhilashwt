from flask import current_app, g
from pymongo import MongoClient

def get_db():
    """Connect to the MongoDB database."""
    if 'db' not in g:
        mongo_url = "mongodb+srv://abhilashnasu:wyvVA5tP78UbEUzf@cluster0.lb4t1nm.mongodb.net/"
        client = MongoClient(mongo_url)
        g.client = client
        g.db = client.library  # 'library' is the database name
        current_app.config['DATABASE'] = g.db
    return g.db

def close_db(e=None):
    """Close the database connection."""
    client = g.pop('client', None)
    if client is not None:
        client.close()

def init_db():
    """Initialize the database with some sample data."""
    db = get_db()
    
    # Check if books collection already has data
    if db.books.count_documents({}) == 0:
        # Add some sample books
        sample_books = [
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'year': 1960,
                'genre': 'Fiction',
                'read': True
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'year': 1949,
                'genre': 'Dystopian',
                'read': False
            },
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'year': 1925,
                'genre': 'Classic',
                'read': True
            }
        ]
        db.books.insert_many(sample_books)
        print("Database initialized with sample data")
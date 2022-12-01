"""
This is a script to create the database. It will be executed only once.
"""
from exts import db
from app import app

with app.app_context():
    db.create_all()  # Create all tables in the database

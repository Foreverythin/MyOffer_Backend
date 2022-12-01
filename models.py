"""
This file defines the structure of table in the database, using ORM.
"""
from exts import db


# Define the Employee class, which is used to store employees' information
class Employee(db.Model):
    __tablename__ = 'employee'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)


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
    logged = db.Column(db.Boolean, nullable=False, default=False)


# Define the Employer class, which is used to store employers' information
class Employer(db.Model):
    __tablename__ = 'employer'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    logged = db.Column(db.Boolean, nullable=False, default=False)


# Define the Captcha class, which is used to store the captcha
class Captcha(db.Model):
    __tablename__ = 'captcha'
    captchaId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(10), nullable=False)
    createdTime = db.Column(db.DateTime, nullable=False)

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
    avatar = db.Column(db.String(200), nullable=False, default='upload/avatar/default.png')
    name = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    age = db.Column(db.Integer, nullable=True, default=18)
    major = db.Column(db.String(50), nullable=True)
    degree = db.Column(db.String(50), nullable=True)
    tel = db.Column(db.String(20), nullable=True)


# Define the Employer class, which is used to store employers' information
class Employer(db.Model):
    __tablename__ = 'employer'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    logged = db.Column(db.Boolean, nullable=False, default=False)
    avatar = db.Column(db.String(200), nullable=False, default='upload/avatar/default.png')


# Define the Captcha class, which is used to store the captcha
class Captcha(db.Model):
    __tablename__ = 'captcha'
    captchaId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(10), nullable=False)
    createdTime = db.Column(db.DateTime, nullable=False)


# Define another captcha table to store the captcha for changing password
class CaptchaPasswordChange(db.Model):
    __tablename__ = 'captchaPasswordChange'
    captchaId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(10), nullable=False)
    createdTime = db.Column(db.DateTime, nullable=False)

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
    resume = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(50), nullable=False, default='Your Name')
    gender = db.Column(db.String(10), nullable=False, default='Male')
    age = db.Column(db.Integer, nullable=False, default=18)
    major = db.Column(db.String(50), nullable=False, default='Your Major')
    degree = db.Column(db.String(50), nullable=False, default='Your Degree')
    tel = db.Column(db.String(20), nullable=False, default='Your Tel')


# Define the Employer class, which is used to store employers' information
class Employer(db.Model):
    __tablename__ = 'employer'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    logged = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(50), nullable=True)
    CEO = db.Column(db.String(50), nullable=True)
    researchDirection = db.Column(db.String(50), nullable=True)
    dateOfEstablishment = db.Column(db.Date, nullable=True)
    location = db.Column(db.String(50), nullable=True)
    staff = db.Column(db.Integer, nullable=True)
    introduction = db.Column(db.String(1000), nullable=True)


# Define the post class, which is used to store posts' information
class Post(db.Model):
    __tablename__ = 'post'
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    label = db.Column(db.String(50), nullable=False)
    tasks = db.Column(db.String(1000), nullable=False)
    requirements = db.Column(db.String(1000), nullable=False)
    inRecruitment = db.Column(db.Boolean, nullable=False, default=True)
    employerId = db.Column(db.Integer, db.ForeignKey('employer.uid'), nullable=False)


# the relationship between post and employee is many-to-many
class PostEmployee(db.Model):
    __tablename__ = 'post_employee'
    pid = db.Column(db.Integer, db.ForeignKey('post.pid'), primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('employee.uid'), primary_key=True)


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

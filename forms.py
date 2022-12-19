"""
This file includes some forms which corresponds to the forms in the frontend.

Data validation is included in the form classes.
"""
from flask import request
import wtforms
from datetime import datetime
from datetime import timedelta
from wtforms import StringField, PasswordField, validators, IntegerField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

from models import Employer, Employee, Captcha


# the form is used to validate the login form
class LoginForm(wtforms.Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])


# the form is used to validate the register form
class RegisterForm(wtforms.Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirmedPassword = PasswordField(
        'Confirmed Password', validators=[DataRequired(), Length(min=6, max=20), EqualTo('password')])
    captcha = StringField('Captcha', validators=[DataRequired(), Length(min=4, max=4)])

    def validateEmail(self, field):
        """
        Check if the email has already existed.
        """
        email = field.data  # get email from request
        employee = Employee.query.filter_by(email=email).first()  # check if the email has already existed in employee table
        if employee:
            raise ValidationError('Email already registered as an identity of an employee')
        employer = Employer.query.filter_by(email=email).first()
        if employer:
            raise ValidationError('Email already registered as an identity of an employer')
        return True

    def validateCaptcha(self, field):
        """
        Check if the captcha is valid.
        """
        captcha = field.data  # get captcha from request
        email = self.email.data  # get email from the form
        captchaModel = Captcha.query.filter_by(email=email).order_by(Captcha.createdTime.desc()).first()
        if not captchaModel or captchaModel.captcha.lower() != captcha.lower() or captchaModel.createdTime + timedelta(
                minutes=5) < datetime.now():
            raise validators.ValidationError('Invalid captcha')
        return True


# the form is used to validate the employee's profile form
class EmployeeProfile(wtforms.Form):
    name = StringField('Name', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), validators.NumberRange(min=18, max=120)])
    major = StringField('Major', validators=[DataRequired()])
    degree = StringField('Degree', validators=[DataRequired()])
    tel = StringField('Tel', validators=[DataRequired(), Length(min=11, max=11)])


# the form is used to validate the employer's profile form
class EmployerProfile(wtforms.Form):
    name = StringField('Name', validators=[DataRequired()])
    CEO = StringField('CEO', validators=[DataRequired()])
    researchDirection = StringField('Research Direction', validators=[DataRequired()])
    dateOfEstablishment = StringField('Date of Establishment', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    staff = IntegerField('Staff', validators=[DataRequired(), validators.NumberRange(min=1, max=100000)])
    introduction = StringField('Introduction', validators=[DataRequired()])


# the form is used to validate the post form
class Post(wtforms.Form):
    title = StringField('Title', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired(), validators.NumberRange(min=2000, max=30000)])
    degree = StringField('Degree', validators=[DataRequired()])
    label = StringField('Label', validators=[DataRequired()])
    tasks = StringField('Tasks', validators=[DataRequired()])
    requirements = StringField('Requirements', validators=[DataRequired()])
    inRecruitment = BooleanField('In Recruitment', validators=[DataRequired()])


# the form is used to validate the post list form
class PostList(wtforms.Form):
    title = StringField('Title', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    salary = IntegerField('Salary', validators=[DataRequired(), validators.NumberRange(min=2000, max=30000)])
    degree = StringField('Degree', validators=[DataRequired()])
    label = StringField('Label', validators=[DataRequired()])
    viewMethod = StringField('View Method', validators=[DataRequired()])

from flask import request
import wtforms
from datetime import datetime
from datetime import timedelta
from wtforms import StringField, PasswordField, validators
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

from models import Employer, Employee, Captcha


class LoginForm(wtforms.Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])


class RegisterForm(wtforms.Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirmedPassword = PasswordField(
        'Confirmed Password', validators=[DataRequired(), Length(min=6, max=20), EqualTo('password')])
    captcha = StringField('Captcha', validators=[DataRequired(), Length(min=4, max=4)])

    def validateEmail(self, field):
        email = field.data
        employee = Employee.query.filter_by(email=email).first()
        if employee:
            raise ValidationError('Email already registered as an identity of employees')
        employer = Employer.query.filter_by(email=email).first()
        if employer:
            raise ValidationError('Email already registered as an identity of employers')
        return True

    def validateCaptcha(self, field):
        captcha = field.data
        email = self.email.data
        captchaModel = Captcha.query.filter_by(email=email).order_by(Captcha.createdTime.desc()).first()
        if not captchaModel or captchaModel.captcha.lower() != captcha.lower() or captchaModel.creatdTime + timedelta(
                minutes=5) < datetime.now():
            raise validators.ValidationError('Invalid captcha')
        return True

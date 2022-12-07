from authlib.jose import jwt
from flask import Blueprint, request, session, jsonify
from flask_restful import Api, Resource, reqparse
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

import string
import random
from datetime import datetime

from forms import LoginForm, RegisterForm
from models import Employer, Employee, Captcha
from exts import db, mail
from config import SECRET_KEY
from utils import generateToken, verifyToken

bp = Blueprint('common', __name__, url_prefix='/')
api = Api(bp)

# the parser is used to parse the request body when users are registering
registerParser = reqparse.RequestParser()
registerParser.add_argument('email', type=str, required=True, help='email cannot be blank!')
registerParser.add_argument('password', type=str, required=True, help='password cannot be blank!')
registerParser.add_argument('confirmedPassword', type=str, required=True, help='confirmedPassword cannot be blank!')
registerParser.add_argument('captcha', type=str, required=True, help='captcha cannot be blank!')

# the parser is used to parse the request body when users are logging in
loginParser = reqparse.RequestParser()
loginParser.add_argument('email', type=str, required=True, help='email cannot be blank!')
loginParser.add_argument('password', type=str, required=True, help='password cannot be blank!')


class Login(Resource):
    def post(self, userType):
        # print the header of the request
        print(request.headers)
        # json to form
        args = loginParser.parse_args()
        form = LoginForm()
        form.email.data = args['email']
        form.password.data = args['password']
        # validate the form
        if form.validate():
            if userType == 'employee':
                employee = Employee.query.filter_by(email=form.email.data).first()
                if employee is None:
                    return jsonify({'status': 400, 'msg': 'Account does not exist!'})
                if check_password_hash(employee.password, form.password.data):
                    # generate a token
                    token = str('employee:') + generateToken(employee.email)
                    employee.logged = True
                    try:
                        db.session.commit()
                    except Exception as e:
                        return jsonify({'status': 403, 'msg': str(e)})
                    return jsonify({'status': 200, 'msg': 'Successfully logged in!', 'token': (token)})
                else:
                    return {'status': 401, 'msg': 'Invalid email or password!'}
            else:
                employer = Employer.query.filter_by(email=form.email.data).first()
                if employer is None:
                    return jsonify({'status': 400, 'msg': 'Account does not exist!'})
                if check_password_hash(employer.password, form.password.data):
                    # generate a token
                    token = str('employer:') + generateToken(employer.email)
                    employer.logged = True
                    try:
                        db.session.commit()
                    except Exception as e:
                        return jsonify({'status': 403, 'msg': str(e)})
                    return jsonify({'status': 200, 'msg': 'Successfully logged in!', 'token': token})
                else:
                    return {'status': 401, 'msg': 'Invalid email or password!'}
        else:
            return {'status': 402, 'msg': form.errors}


class Register(Resource):
    def post(self, userType):
        args = registerParser.parse_args()
        form = RegisterForm()
        form.email.data = args['email']
        form.password.data = args['password']
        form.confirmedPassword.data = args['confirmedPassword']
        form.captcha.data = args['captcha']
        try:
            if form.validate() and form.validateEmail(form.email) and form.validateCaptcha(form.captcha):
                if userType == 'employee':
                    hashPassword = generate_password_hash(form.password.data)
                    employee = Employee(email=form.email.data, password=hashPassword)
                    db.session.add(employee)
                else:
                    hashPassword = generate_password_hash(form.password.data)
                    employer = Employer(email=form.email.data, password=hashPassword)
                    db.session.add(employer)
                try:
                    db.session.commit()
                    return jsonify({'status': 200, 'msg': 'Successfully registered!'})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'status': 403, 'msg': 'Failed to register! ' + str(e)})
            else:
                return jsonify({'status': 402, 'msg': form.errors})
        except Exception as e:
            return jsonify({'status': 404, 'msg': 'Failed to register! ' + str(e)})


class GetCaptcha(Resource):
    def get(self):
        print('i am here')
        print(request.headers.get('Authorization'))
        # get the parameters from the request
        email = request.args.get('email')
        User = Employee.query.filter_by(email=email).first()
        if User:
            return jsonify({'status': 405, 'msg': 'Account already exists as an identity of an employee!'})
        User = Employer.query.filter_by(email=email).first()
        if User:
            return jsonify({'status': 405, 'msg': 'Account already exists as an identity of an employer!'})
        letters = string.ascii_letters + string.digits  # Get all the letters and numbers.
        captcha = "".join(random.sample(letters, 4))  # Generate a random captcha.
        message = Message('Captcha', recipients=[email], body="The captcha is: " + captcha + ", just valid for 5 "
                                                                                                "minutes.")

        captchaModel = Captcha.query.filter_by(email=email).first()
        if captchaModel:
            captchaModel.captcha = captcha
            captchaModel.createdTime = datetime.now()
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 403, 'msg': 'Failed to send captcha! ' + str(e)})
        else:
            captchaModel = Captcha(email=email, captcha=captcha, createdTime=datetime.now())
            db.session.add(captchaModel)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({'status': 403, 'msg': 'Failed to send captcha! ' + str(e)})

        mail.send(message)

        return jsonify({'status': 200, 'msg': 'Captcha has been sent to your email address!'})


class Logout(Resource):
    @verifyToken
    def get(self, userType):
        token = request.headers.get('Authorization')[9:]
        token = bytes(token, encoding='utf-8')
        payload = jwt.decode(token, SECRET_KEY)
        if userType == 'employee':
            employee = Employee.query.filter_by(email=payload['email']).first()
            employee.logged = False
            try:
                db.session.commit()
            except Exception as e:
                return jsonify({'status': 403, 'msg': str(e)})
            return jsonify({'status': 200, 'msg': 'Successfully logged out!'})
        elif userType == 'employer':
            employer = Employer.query.filter_by(email=payload['email']).first()
            employer.logged = False
            try:
                db.session.commit()
            except Exception as e:
                return jsonify({'status': 403, 'msg': str(e)})
            return jsonify({'status': 200, 'msg': 'Successfully logged out!'})
        else:
            return jsonify({'status': 407, 'msg': 'Invalid url!'})


class Test(Resource):
    @verifyToken
    def get(self, userType):
        return jsonify({'status': 200, 'msg': 'A Successful Test.'})


api.add_resource(Register, '/register/<string:userType>')
api.add_resource(Login, '/login/<string:userType>')
api.add_resource(GetCaptcha, '/captcha')
api.add_resource(Test, '/test/<string:userType>')
api.add_resource(Logout, '/logout/<string:userType>')

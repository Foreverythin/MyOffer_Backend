from authlib.jose import jwt
from flask import Blueprint, request, session, jsonify, send_file, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

import os
import string
import random
from datetime import datetime

from forms import LoginForm, RegisterForm
from models import Employer, Employee, Captcha
from exts import db, mail
from config import SECRET_KEY
from utils import generateToken, verifyToken

AVATAR_UPLOAD_FOLDER = 'upload/avatar/'

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


class Avatar(Resource):
    def get(self, userType, tokenStr):
        token = tokenStr[9:]
        token = bytes(token, encoding='utf-8')
        payload = jwt.decode(token, SECRET_KEY)
        if userType == 'employee':
            employee = Employee.query.filter_by(email=payload['email']).first()
            if employee:
                return send_file(employee.avatar, mimetype='image')
            else:
                return jsonify({'status': 406, 'msg': 'Invalid token!'})
        elif userType == 'employer':
            employer = Employer.query.filter_by(email=payload['email']).first()
            if employer:
                return send_file(employer.avatar, mimetype='image')
            else:
                return jsonify({'status': 406, 'msg': 'Invalid token!'})
        else:
            return send_file('/upload/avatar/default.png', mimetype='image')

    def post(self, userType, tokenStr):
        token = tokenStr[9:]
        token = bytes(token, encoding='utf-8')
        payload = jwt.decode(token, SECRET_KEY)
        avatar = request.files.get('file')
        if not avatar:
            return jsonify({'status': 402, 'msg': 'No file uploaded!'})
        if userType == 'employee':
            employee = Employee.query.filter_by(email=payload['email']).first()
            if employee:
                # change the name of the avatar
                avatarName = str(employee.email + '.' + avatar.filename.split('.')[-1])
                # save the avatar
                avatar.save(os.path.join(AVATAR_UPLOAD_FOLDER, avatarName))
                # update the avatar in the database
                employee.avatar = os.path.join(AVATAR_UPLOAD_FOLDER, avatarName)
                try:
                    db.session.commit()
                    return jsonify({'status': 200, 'msg': 'Successfully updated!'})
                except Exception as e:
                    return jsonify({'status': 403, 'msg': 'Failed to update! ' + str(e)})
            else:
                return jsonify({'status': 410, 'msg': 'Login in firstly!'})
        elif userType == 'employer':
            employer = Employer.query.filter_by(email=payload['email']).first()
            if employer:
                # change the name of the avatar
                avatarName = str(employer.email + '.' + avatar.filename.split('.')[-1])
                # save the avatar
                avatar.save(os.path.join(AVATAR_UPLOAD_FOLDER, avatarName))
                # update the avatar in the database
                employer.avatar = os.path.join(AVATAR_UPLOAD_FOLDER, avatarName)
                try:
                    db.session.commit()
                    return jsonify({'status': 200, 'msg': 'Successfully updated!'})
                except Exception as e:
                    return jsonify({'status': 403, 'msg': 'Failed to update! ' + str(e)})
            else:
                return jsonify({'status': 410, 'msg': 'Login in firstly!'})
        else:
            return jsonify({'status': 410, 'msg': 'Login in firstly!'})


# class UpdateAvatar(Resource):
#     @verifyToken
#     def post(self, userType):
#         print(1)
#         avatar = request.files['avatar']
#         print(avatar)
#         return jsonify({'status': 200, 'msg': 'Successfully updated!'})


api.add_resource(Register, '/register/<string:userType>')
api.add_resource(Login, '/login/<string:userType>')
api.add_resource(GetCaptcha, '/captcha')
api.add_resource(Avatar, '/avatar/<string:userType>/<string:tokenStr>')
# api.add_resource(UpdateAvatar, '/updateAvatar/<string:userType>')
api.add_resource(Logout, '/logout/<string:userType>')

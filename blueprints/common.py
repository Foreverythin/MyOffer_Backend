from authlib.jose import jwt
from flask import Blueprint, request, session, jsonify, send_file, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

import os
import string
import random
from datetime import datetime

from app import app
from forms import LoginForm, RegisterForm
from models import Employer, Employee, Captcha, CaptchaPasswordChange
from exts import db, mail, logger
from config import SECRET_KEY
from utils import generateToken, verifyToken, emailByTokenStr

AVATAR_UPLOAD_FOLDER = 'upload/avatar/'
LETTRES = string.ascii_letters + string.digits  # Containing all letters and numbers.

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
                    logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                        request.remote_addr, form.email.data,
                        'The email is not registered when logging in!'))
                    return jsonify({'status': 400, 'msg': 'Account does not exist!'})
                if check_password_hash(employee.password, form.password.data):
                    # generate a token
                    token = str('employee:') + generateToken(employee.email)
                    employee.logged = True
                    try:
                        db.session.commit()
                        logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                            request.remote_addr, form.email.data,
                            'The user logged in successfully as an employee!'))
                    except Exception as e:
                        logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                            request.remote_addr, form.email.data,
                            'The user logged in failed, because of %s' % e))
                        db.session.rollback()
                        return jsonify({'status': 403, 'msg': str(e)})
                    return jsonify({'status': 200, 'msg': 'Successfully logged in!', 'token': (token)})
                else:
                    logger.warning('[IP] - %s, [email] - %s, [password] - %s, [msg] - %s' % (
                        request.remote_addr, form.email.data, form.password.data,
                        'The password is wrong when logging in!'))
                    return jsonify({'status': 401, 'msg': 'Invalid email or password!'})
            else:
                employer = Employer.query.filter_by(email=form.email.data).first()
                if employer is None:
                    logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                        request.remote_addr, form.email.data,
                        'The email is not registered when logging in!'))
                    return jsonify({'status': 400, 'msg': 'Account does not exist!'})
                if check_password_hash(employer.password, form.password.data):
                    # generate a token
                    token = str('employer:') + generateToken(employer.email)
                    employer.logged = True
                    try:
                        db.session.commit()
                        logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                            request.remote_addr, form.email.data,
                            'The user logged in successfully as an employer!'))
                    except Exception as e:
                        logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                            request.remote_addr, form.email.data,
                            'The user logged in failed, because of %s' % e))
                        db.session.rollback()
                        return jsonify({'status': 403, 'msg': str(e)})
                    return jsonify({'status': 200, 'msg': 'Successfully logged in!', 'token': token})
                else:
                    logger.warning('[IP] - %s, [email] - %s, [password] - %s, [msg] - %s' % (
                        request.remote_addr, form.email.data, form.password.data,
                        'The password is wrong when logging in!'))
                    return jsonify({'status': 401, 'msg': 'Invalid email or password!'})
        else:
            logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, form.email.data,
                'The form is not valid when logging in: %s!' % form.errors))
            return jsonify({'status': 402, 'msg': form.errors})


class Register(Resource):
    def post(self, userType):
        args = registerParser.parse_args()
        form = RegisterForm()
        form.email.data = args['email']
        form.password.data = args['password']
        form.confirmedPassword.data = args['confirmedPassword']
        form.captcha.data = args['captcha']
        if len(form.password.data) < 6 or len(form.password.data) > 18:
            return jsonify({'status': 402, 'msg': 'The length of password should be between 6 and 18!'})
        if form.password.data != form.confirmedPassword.data:
            return jsonify({'status': 402, 'msg': 'The two passwords are not the same!'})
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
                    logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                        request.remote_addr, form.email.data,
                        'The user registered successfully as an %s!' % userType))
                    return jsonify({'status': 200, 'msg': 'Successfully registered!'})
                except Exception as e:
                    logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                        request.remote_addr, form.email.data,
                        'The user registered failed, because of %s' % e))
                    db.session.rollback()
                    return jsonify({'status': 403, 'msg': 'Failed to register! ' + str(e)})
            else:
                logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, form.email.data,
                    'The form is not valid when registering: %s' % form.errors))
                return jsonify({'status': 402, 'msg': form.errors})
        except Exception as e:
            logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, form.email.data,
                'The user registered failed, because of %s' % e))
            return jsonify({'status': 404, 'msg': 'Failed to register! ' + str(e)})


class GetCaptcha(Resource):
    def get(self):
        # get the parameters from the request
        email = request.args.get('email')
        User = Employee.query.filter_by(email=email).first()
        if User:
            logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, email,
                'The email is already registered as an employee, so the captcha cannot be sent!'))
            return jsonify({'status': 405, 'msg': 'Account already exists as an identity of an employee!'})
        User = Employer.query.filter_by(email=email).first()
        if User:
            logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, email,
                'The email is already registered as an employer, so the captcha cannot be sent!'))
            return jsonify({'status': 405, 'msg': 'Account already exists as an identity of an employer!'})
        captcha = "".join(random.sample(LETTRES, 4))  # Generate a random captcha.
        message = Message('Captcha', recipients=[email], body="The captcha is: " + captcha + ", just valid for 5 "
                                                                                             "minutes.")

        captchaModel = Captcha.query.filter_by(email=email).first()
        if captchaModel:
            captchaModel.captcha = captcha
            captchaModel.createdTime = datetime.now()
            try:
                db.session.commit()
                logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, email,
                    'The captcha is updated successfully in the database!'))
            except Exception as e:
                db.session.rollback()
                logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, email,
                    'The captcha is updated failed, because of %s' % e))
                return jsonify({'status': 403, 'msg': 'Failed to send captcha! ' + str(e)})
        else:
            captchaModel = Captcha(email=email, captcha=captcha, createdTime=datetime.now())
            db.session.add(captchaModel)
            try:
                db.session.commit()
                logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, email,
                    'The captcha is added successfully in the database!'))
            except Exception as e:
                db.session.rollback()
                logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, email,
                    'The captcha is added failed, because of %s' % e))
                return jsonify({'status': 403, 'msg': 'Failed to send captcha! ' + str(e)})

        mail.send(message)
        logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
            request.remote_addr, email,
            'The captcha is sent successfully when registering!'))

        return jsonify({'status': 200, 'msg': 'Captcha has been sent to your email address!'})


class Logout(Resource):
    @verifyToken
    def get(self, userType):
        token = request.headers.get('Authorization')[9:]
        token = bytes(token, encoding='utf-8')
        payload = jwt.decode(token, SECRET_KEY)
        if userType == 'employee':
            employee = Employee.query.filter_by(email=payload['email']).first()
            if not employee:
                logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'Wrong email when logging out as an employee!'))
                return jsonify({'status': 401, 'msg': 'The user is not an employee!'})
            if employee.logged is False:
                logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The user has already logged out as an employee!'))
                return jsonify({'status': 414, 'msg': 'The user has already logged out!'})
            employee.logged = False
            try:
                db.session.commit()
                logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The employee logged out successfully!'))
            except Exception as e:
                db.session.rollback()
                logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The employee logged out failed, because of %s' % e))
                return jsonify({'status': 403, 'msg': str(e)})
            return jsonify({'status': 200, 'msg': 'Successfully logged out!'})
        elif userType == 'employer':
            employer = Employer.query.filter_by(email=payload['email']).first()
            if not employer:
                logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'Wrong email when logging out as an employer!'))
                return jsonify({'status': 401, 'msg': 'The user is not an employer!'})
            if employer.logged is False:
                logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The user has already logged out as an employer!'))
                return jsonify({'status': 414, 'msg': 'The user has already logged out!'})
            employer.logged = False
            try:
                db.session.commit()
                logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The employer logged out successfully!'))
            except Exception as e:
                db.session.rollback()
                logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The employer logged out failed, because of %s' % e))
                return jsonify({'status': 403, 'msg': str(e)})
            return jsonify({'status': 200, 'msg': 'Successfully logged out!'})
        else:
            logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, payload['email'],
                'The user logged out failed, because of %s' % 'The user type is not correct!'))
            return jsonify({'status': 407, 'msg': 'Invalid url!'})


class Avatar(Resource):
    def get(self, userType, tokenStr):
        token = tokenStr[9:]
        token = bytes(token, encoding='utf-8')
        payload = jwt.decode(token, SECRET_KEY)
        if userType == 'employee':
            employee = Employee.query.filter_by(email=payload['email']).first()
            if employee:
                logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The employee avatar is got successfully!'))
                return send_file(AVATAR_UPLOAD_FOLDER + employee.avatar, mimetype='image')
            else:
                logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The employee avatar is got failed, because of %s' % 'The employee does not exist or has logged out!'))
                return jsonify({'status': 406, 'msg': 'Invalid token!'})
        elif userType == 'employer':
            employer = Employer.query.filter_by(email=payload['email']).first()
            if employer:
                logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The employer avatar is got successfully!'))
                return send_file(AVATAR_UPLOAD_FOLDER + employer.avatar, mimetype='image')
            else:
                logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The employer avatar is got failed, because of %s' % 'The employer does not exist or has logged out!'))
                return jsonify({'status': 406, 'msg': 'Invalid token!'})
        else:
            return send_file(AVATAR_UPLOAD_FOLDER + 'default.png', mimetype='image')

    def post(self, userType, tokenStr):
        token = tokenStr[9:]
        token = bytes(token, encoding='utf-8')
        payload = jwt.decode(token, SECRET_KEY)
        avatar = request.files.get('file')
        if not avatar:
            logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, payload['email'],
                'The avatar is uploaded failed, because of %s' % 'The avatar file is empty!'))
            return jsonify({'status': 402, 'msg': 'No file uploaded!'})
        if userType == 'employee':
            employee = Employee.query.filter_by(email=payload['email']).first()
            if employee:
                # change the name of the avatar
                avatarName = str(employee.email + '.' + avatar.filename.split('.')[-1])
                # save the avatar
                avatar.save(os.path.join(AVATAR_UPLOAD_FOLDER, avatarName))
                # update the avatar in the database
                employee.avatar = avatarName
                try:
                    db.session.commit()
                    logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                        request.remote_addr, payload['email'],
                        'The employee avatar is uploaded successfully!'))
                    return jsonify({'status': 200, 'msg': 'Successfully updated!'})
                except Exception as e:
                    db.session.rollback()
                    logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                        request.remote_addr, payload['email'],
                        'The employee avatar is uploaded failed, because of %s' % e))
                    return jsonify({'status': 403, 'msg': 'Failed to update! ' + str(e)})
            else:
                logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The employee avatar is uploaded failed, because of %s' % 'The employee does not exist or has logged out!'))
                return jsonify({'status': 410, 'msg': 'Login in firstly!'})
        elif userType == 'employer':
            employer = Employer.query.filter_by(email=payload['email']).first()
            if employer:
                # change the name of the avatar
                avatarName = str(employer.email + '.' + avatar.filename.split('.')[-1])
                # save the avatar
                avatar.save(os.path.join(AVATAR_UPLOAD_FOLDER, avatarName))
                # update the avatar in the database
                employer.avatar = avatarName
                try:
                    db.session.commit()
                    logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                        request.remote_addr, payload['email'],
                        'The employer avatar is uploaded successfully!'))
                    return jsonify({'status': 200, 'msg': 'Successfully updated!'})
                except Exception as e:
                    db.session.rollback()
                    logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                        request.remote_addr, payload['email'],
                        'The employer avatar is uploaded failed, because of %s' % e))
                    return jsonify({'status': 403, 'msg': 'Failed to update! ' + str(e)})
            else:
                logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, payload['email'],
                    'The employer avatar is uploaded failed, because of %s' % 'The employer does not exist or has logged out!'))
                return jsonify({'status': 410, 'msg': 'Login in firstly!'})
        else:
            logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, payload['email'],
                'The avatar is uploaded failed, because of %s' % 'The user type is invalid!'))
            return jsonify({'status': 410, 'msg': 'Login in firstly!'})


class changePassword(Resource):
    @verifyToken
    def put(self, userType):
        token = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(token)
        captchaModel = CaptchaPasswordChange.query.filter_by(email=email).first()
        if captchaModel:
            if captchaModel.captcha.lower() == request.json.get('captcha').lower():
                if (datetime.now() - captchaModel.createdTime).seconds < 300:
                    if userType == 'employee':
                        employee = Employee.query.filter_by(email=email).first()
                        hashPassword = generate_password_hash(request.json.get('password'))
                        employee.password = hashPassword
                        try:
                            db.session.commit()
                            logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                                request.remote_addr, email,
                                'The employee password is changed successfully!'))
                            return jsonify({'status': 200, 'msg': 'Successfully changed!'})
                        except Exception as e:
                            db.session.rollback()
                            logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                                request.remote_addr, email,
                                'The employee password is changed failed, because of %s' % e))
                            return jsonify({'status': 403, 'msg': 'Failed to change! ' + str(e)})
                    elif userType == 'employer':
                        employer = Employer.query.filter_by(email=email).first()
                        hashPassword = generate_password_hash(request.json.get('password'))
                        employer.password = hashPassword
                        try:
                            db.session.commit()
                            logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                                request.remote_addr, email,
                                'The employer password is changed successfully!'))
                            return jsonify({'status': 200, 'msg': 'Successfully changed!'})
                        except Exception as e:
                            db.session.rollback()
                            logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                                request.remote_addr, email,
                                'The employer password is changed failed, because of %s' % e))
                            return jsonify({'status': 403, 'msg': 'Failed to change! ' + str(e)})
                    else:
                        logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                            request.remote_addr, email,
                            'The password is changed failed, because of %s' % 'The user type is invalid!'))
                        return jsonify({'status': 407, 'msg': 'Invalid url!'})
                else:
                    logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                        request.remote_addr, email,
                        'The password is changed failed, because of %s' % 'the captcha is expired!'))
                    return jsonify({'status': 405, 'msg': 'Captcha expired!'})
            else:
                logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, email,
                    'The password is changed failed, because of %s' % 'the captcha is invalid!'))
                return jsonify({'status': 404, 'msg': 'Invalid captcha!'})

    @verifyToken
    def get(self, userType):
        token = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(token)
        captcha = "".join(random.sample(LETTRES, 4))  # Generate a random captcha.
        message = Message('Captcha', recipients=[email], body="The captcha is: " + captcha + ", just valid for 5 "
                                                                                             "minutes.")
        # check if the email has been sent captcha before
        captchaModel = CaptchaPasswordChange.query.filter_by(email=email).first()
        if captchaModel:
            captchaModel.captcha = captcha
            captchaModel.createdTime = datetime.now()
            try:
                db.session.commit()
                logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, email,
                    'The captcha is sent successfully!'))
            except Exception as e:
                db.session.rollback()
                logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, email,
                    'The captcha is sent failed, because of %s' % e))
                return jsonify({'status': 403, 'msg': 'Failed to send captcha! ' + str(e)})
        else:
            captchaModel = CaptchaPasswordChange(email=email, captcha=captcha, createdTime=datetime.now())
            db.session.add(captchaModel)
            try:
                db.session.commit()
                logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, email,
                    'The captcha is sent successfully!'))
            except Exception as e:
                db.session.rollback()
                logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                    request.remote_addr, email,
                    'The captcha is sent failed, because of %s' % e))
                return jsonify({'status': 403, 'msg': 'Failed to send captcha! ' + str(e)})
        mail.send(message)

        return jsonify({'status': 200, 'msg': 'Captcha has been sent to your email address!'})


api.add_resource(Register, '/register/<string:userType>')
api.add_resource(Login, '/login/<string:userType>')
api.add_resource(GetCaptcha, '/captcha')
api.add_resource(Avatar, '/avatar/<string:userType>/<string:tokenStr>')
api.add_resource(Logout, '/logout/<string:userType>')
api.add_resource(changePassword, '/changePassword/<string:userType>')

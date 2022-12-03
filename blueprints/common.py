from flask import Blueprint, request, session, jsonify
from flask_restful import Api, Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash

from forms import LoginForm, RegisterForm
from models import Employer, Employee
from exts import db, mail

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

# the parser is used to parse the request body when users are requiring a captcha
captchaParser = reqparse.RequestParser()
captchaParser.add_argument('email', type=str, required=True, help='email cannot be blank!')


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
                    return jsonify({'status': 400, 'msg': 'Account does not exist!'})
                if check_password_hash(employee.password, form.password.data):
                    session['employeeId'] = employee.uid
                    return jsonify({'status': 200, 'msg': 'Successfully logged in!'})
                else:
                    return {'status': 401, 'msg': 'Invalid email or password!'}
            else:
                employer = Employer.query.filter_by(email=form.email.data).first()
                if employer is None:
                    return jsonify({'status': 400, 'msg': 'Account does not exist!'})
                if check_password_hash(employer.password, form.password.data):
                    session['employerId'] = employer.uid
                    return jsonify({'status': 200, 'msg': 'Successfully logged in!'})
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
    def get(self, userType):
        args = captchaParser.parse_args()
        return {'message': 'Captcha sent'}


api.add_resource(Register, '/register/<string:userType>')
api.add_resource(Login, '/login/<string:userType>')
api.add_resource(GetCaptcha, '/captcha/<string:userType>')


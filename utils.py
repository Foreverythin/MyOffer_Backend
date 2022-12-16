from authlib.jose import jwt, JoseError
from functools import wraps
from config import SECRET_KEY
from flask import request, jsonify

from models import Employee, Employer


def generateToken(email):
    header = {'alg': 'HS256'}
    payload = {'email': email}
    token = jwt.encode(header, payload, SECRET_KEY)
    tokenStr = str(token, encoding='utf-8')

    return tokenStr


# define a decorator to check the token: employee and employer
def verifyToken(func):
    def wrapper(self, userType, *args, **kwargs):
        tokenStr = request.headers.get('Authorization')
        if tokenStr is None:
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
        token = tokenStr[9:]
        token = bytes(token, encoding="utf8")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
                if userType == 'employee':
                    employee = Employee.query.filter_by(email=payload['email']).first()
                    if employee and employee.logged:
                        return func(self, userType)
                    else:
                        return jsonify({'status': 410, 'msg': 'Please log in first!'})
                elif userType == 'employer':
                    employer = Employer.query.filter_by(email=payload['email']).first()
                    if employer and employer.logged:
                        return func(self, userType)
                    else:
                        return jsonify({'status': 410, 'msg': 'Please log in first!'})
                else:
                    return jsonify({'status': 410, 'msg': 'Please log in first!'})
            except JoseError as e:
                return jsonify({'status': 409, 'msg': 'Please log in first!'})
        else:
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
    return wrapper


# define a decorator to check the token: employee
def verifyEmployeeToken(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        tokenStr = request.headers.get('Authorization')
        if tokenStr is None:
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
        token = tokenStr[9:]
        token = bytes(token, encoding="utf8")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
                employee = Employee.query.filter_by(email=payload['email']).first()
                if employee and employee.logged:
                    return func(self, *args, **kwargs)
                else:
                    return jsonify({'status': 410, 'msg': 'Please log in first!'})
            except JoseError as e:
                return jsonify({'status': 409, 'msg': 'Please log in first!'})
        else:
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
    return wrapper


# define a decorator to check the token: employer
def verifyEmployerToken(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        tokenStr = request.headers.get('Authorization')
        if tokenStr is None:
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
        token = tokenStr[9:]
        token = bytes(token, encoding="utf8")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
                employer = Employer.query.filter_by(email=payload['email']).first()
                if employer and employer.logged:
                    return func(self, *args, **kwargs)
                else:
                    return jsonify({'status': 410, 'msg': 'Please log in first!'})
            except JoseError as e:
                return jsonify({'status': 409, 'msg': 'Please log in first!'})
        else:
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
    return wrapper


def emailByTokenStr(tokenStr):
    token = bytes(tokenStr, encoding="utf8")
    payload = jwt.decode(token, SECRET_KEY)
    email = payload.get('email')

    return email

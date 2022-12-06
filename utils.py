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


# define a decorator to check the token
def verifyToken(func):
    def wrapper(self, userType):
        tokenStr = request.headers.get('Authorization')
        token = tokenStr[9:]
        print(type(token))
        token = bytes(token, encoding="utf8")
        print(type(token))
        print(token)
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
                print('userType: ', userType)
                if userType == 'employee':
                    employee = Employee.query.filter_by(email=payload['email']).first()
                    if employee and employee.logged:
                        return func(self, userType)
                    else:
                        return jsonify({'status': 410, 'msg': 'Please log in first!'})
                elif userType == 'employer':
                    employer = Employer.query.filter_by(email=payload['email']).first()
                    if employer and employer.logged:
                        return func(userType)
                    else:
                        return jsonify({'status': 410, 'msg': 'Please log in first!'})
                else:
                    return jsonify({'status': 410, 'msg': 'Please log in first!'})
            except JoseError as e:
                return jsonify({'status': 409, 'msg': 'Please log in first!'})
        else:
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
    return wrapper

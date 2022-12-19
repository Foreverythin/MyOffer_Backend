"""
The file defines some tool functions which will be used in the blueprints.
"""
from authlib.jose import jwt, JoseError
from functools import wraps
from config import SECRET_KEY
from flask import request, jsonify
import re

from models import Employee, Employer


def generateToken(email):
    """
    Generate a token for the user with the email.
    """
    header = {'alg': 'HS256'}
    payload = {'email': email}
    token = jwt.encode(header, payload, SECRET_KEY)
    tokenStr = str(token, encoding='utf-8')

    return tokenStr


def verifyToken(func):
    """
    Define a decorator to check the token: employee and employer
    """
    def wrapper(self, userType, *args, **kwargs):
        tokenStr = request.headers.get('Authorization')  # get the token from the header
        if tokenStr is None:  # no token
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
        token = tokenStr[9:]
        token = bytes(token, encoding="utf8")  # convert the token to bytes
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)  # decode the token
                if userType == 'employee':  # check the user type
                    employee = Employee.query.filter_by(email=payload['email']).first()
                    if employee and employee.logged:  # check if the user has logged in
                        return func(self, userType)  # call the function
                    else:
                        return jsonify({'status': 410, 'msg': 'Please log in first!'})
                elif userType == 'employer':  # check the user type
                    employer = Employer.query.filter_by(email=payload['email']).first()
                    if employer and employer.logged:  # check if the user has logged in
                        return func(self, userType)  # call the function
                    else:
                        return jsonify({'status': 410, 'msg': 'Please log in first!'})
                else:
                    return jsonify({'status': 410, 'msg': 'Please log in first!'})
            except JoseError as e:
                return jsonify({'status': 409, 'msg': 'Please log in first!'})
        else:
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
    return wrapper


def verifyEmployeeToken(func):
    """
    Define a decorator to check the token: employee.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        tokenStr = request.headers.get('Authorization')  # get the token from the header
        if tokenStr is None:  # no token
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
        token = tokenStr[9:]
        token = bytes(token, encoding="utf8")  # convert the token to bytes
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)   # decode the token
                employee = Employee.query.filter_by(email=payload['email']).first()  # get the user
                if employee and employee.logged:  # check if the user has logged in
                    return func(self, *args, **kwargs)  # call the function
                else:
                    return jsonify({'status': 410, 'msg': 'Please log in first!'})
            except JoseError as e:
                return jsonify({'status': 409, 'msg': 'Please log in first!'})
        else:
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
    return wrapper


def verifyEmployerToken(func):
    """
    Define a decorator to check the token: employer.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        tokenStr = request.headers.get('Authorization')  # get the token from the header
        if tokenStr is None:  # no token
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
        token = tokenStr[9:]
        token = bytes(token, encoding="utf8")  # convert the token to bytes
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)  # decode the token
                employer = Employer.query.filter_by(email=payload['email']).first()  # get the user
                if employer and employer.logged:  # check if the user has logged in
                    return func(self, *args, **kwargs)  # call the function
                else:
                    return jsonify({'status': 410, 'msg': 'Please log in first!'})
            except JoseError as e:
                return jsonify({'status': 409, 'msg': 'Please log in first!'})
        else:
            return jsonify({'status': 410, 'msg': 'Please log in first!'})
    return wrapper


def emailByTokenStr(tokenStr):
    """
    Get the email from the token string.
    """
    token = bytes(tokenStr, encoding="utf8")
    payload = jwt.decode(token, SECRET_KEY)
    email = payload.get('email')

    return email


def validTel(telStr):
    """
    Check if the telephone number is valid.
    """
    if re.match(r'^1[3-9]\d{9}$', telStr):
        return True
    else:
        return False

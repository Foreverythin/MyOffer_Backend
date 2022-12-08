from authlib.jose import jwt
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from models import Employee

from config import SECRET_KEY
from utils import verifyEmployeeToken

bp = Blueprint('employee', __name__, url_prefix='/employee')
api = Api(bp)


class EmployeeList(Resource):
    def get(self):
        return {'employees': ['John', 'Jane', 'Joe']}

    def post(self):
        return {'message': 'Employee created'}


class Profile(Resource):
    @verifyEmployeeToken
    def put(self):
        return jsonify({'status': 200, 'msg': 'Profile updated successfully!'})

    @verifyEmployeeToken
    def get(self):
        token = request.headers.get('Authorization')[9:]
        token = bytes(token, encoding='utf-8')
        payload = jwt.decode(token, SECRET_KEY)
        email = payload.get('email')
        employee = Employee.query.filter_by(email=email).first()
        name = employee.name
        gender = employee.gender
        age = employee.age
        major = employee.major
        degree = employee.degree
        tel = employee.tel
        return jsonify({'status': 200, 'msg': 'Profile fetched successfully!', 'data':
            {'email': email, 'name': name, 'gender': gender, 'age': age, 'major': major, 'degree': degree, 'tel': tel}})


api.add_resource(EmployeeList, '/list')
api.add_resource(Profile, '/profile')

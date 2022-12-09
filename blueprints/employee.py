from authlib.jose import jwt
from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from models import Employee
from exts import db

from config import SECRET_KEY
from utils import verifyEmployeeToken, emailByTokenStr

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
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
        employee = Employee.query.filter_by(email=email).first()
        employee.name = request.json.get('name')
        employee.gender = request.json.get('gender')
        employee.age = request.json.get('age')
        employee.major = request.json.get('major')
        employee.degree = request.json.get('degree')
        employee.tel = request.json.get('tel')
        try:
            db.session.commit()
            return jsonify({'status': 200, 'msg': 'Update profile successfully!'})
        except Exception as e:
            return jsonify({'status': 403, 'msg': str(e)})

    @verifyEmployeeToken
    def get(self):
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
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

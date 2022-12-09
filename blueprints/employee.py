import os
from authlib.jose import jwt

from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource

from models import Employee
from exts import db

from config import SECRET_KEY
from utils import verifyEmployeeToken, emailByTokenStr

RESUME_UPLOAD_FOLDER = 'upload/resume/'

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


class Resume(Resource):
    @verifyEmployeeToken
    def post(self):
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
        resume = request.files.get('file')
        resumeFileName = email + '_' + resume.filename
        # delete the old resume
        employee = Employee.query.filter_by(email=email).first()
        if employee.resume:
            os.remove(RESUME_UPLOAD_FOLDER + employee.resume)
        resume.save(os.path.join(RESUME_UPLOAD_FOLDER, resumeFileName))
        employee.resume = resumeFileName
        try:
            db.session.commit()
            return jsonify({'status': 200, 'msg': 'Upload resume successfully!'})
        except Exception as e:
            return jsonify({'status': 403, 'msg': str(e)})

    @verifyEmployeeToken
    def get(self):
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
        employee = Employee.query.filter_by(email=email).first()
        if employee.resume is not None:
            _index = employee.resume.index('_')
            resumeFileName = employee.resume[_index + 1:]
            return jsonify({'status': 200, 'msg': 'Resume fetched successfully!', 'data': {'resume': resumeFileName}})
        else:
            return jsonify({'status': 200, 'msg': 'Resume fetched successfully!', 'data': {'resume': 'No File Uploaded'}})


api.add_resource(EmployeeList, '/list')
api.add_resource(Profile, '/profile')
api.add_resource(Resume, '/resume')

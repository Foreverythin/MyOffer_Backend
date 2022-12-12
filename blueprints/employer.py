from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with

import datetime

from models import Employer
from exts import db

from utils import verifyToken, generateToken, verifyEmployerToken, emailByTokenStr

bp = Blueprint('employer', __name__, url_prefix='/employer')
api = Api(bp)

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name cannot be blank!')
parser.add_argument('age', type=int, required=True, help='Age cannot be blank!')

fields = {
    'name': fields.Integer,
    'age': fields.Integer
}


class EmployerList(Resource):
    @marshal_with(fields)
    def get(self):
        return {'employers': ['John', 'Jane', 'Joe']}

    def post(self):
        # get the data from the request
        args = parser.parse_args()
        name = args['name']
        age = args['age']
        gender = args.get('gender')
        return {'message': 'Employer created', 'name': name, 'age': age, 'gender': gender}
        # args = parser.parse_args()
        # print(args)
        # return {'message': 'Employer created', 'data': args.get('name')}


class BasicInfo(Resource):
    @verifyEmployerToken
    def post(self):
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
        employer = Employer.query.filter_by(email=email).first()
        employer.name = request.json.get('name')
        employer.CEO = request.json.get('CEO')
        employer.researchDirection = request.json.get('researchDirection')
        try:
            employer.dateOfEstablishment = datetime.datetime.strptime(request.json.get('dateOfEstablishment')[:10], '%Y-%m-%d')
        except Exception as e:
            print(str(e))
            employer.dateOfEstablishment = None
        employer.location = request.json.get('location')
        employer.staff = request.json.get('staff')
        try:
            db.session.commit()
            return jsonify({'status': 200, 'msg': 'Update profile successfully!',
                            'data' :{'email': email, 'name': employer.name, 'CEO': employer.CEO, 'researchDirection': employer.researchDirection, 'dateOfEstablishment': employer.dateOfEstablishment, 'location': employer.location, 'staff': employer.staff}})
        except Exception as e:
            return jsonify({'status': 403, 'msg': str(e)})

    @verifyEmployerToken
    def get(self):
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
        employer = Employer.query.filter_by(email=email).first()
        name = employer.name
        CEO = employer.CEO
        researchDirection = employer.researchDirection
        dateOfEstablishment = employer.dateOfEstablishment
        location = employer.location
        staff = employer.staff
        return jsonify({'status': 200, 'msg': 'Profile fetched successfully!', 'data':
            {'email': email, 'name': name, 'CEO': CEO, 'researchDirection': researchDirection, 'dateOfEstablishment': dateOfEstablishment, 'location': location, 'staff': staff}})


api.add_resource(EmployerList, '/list')
api.add_resource(BasicInfo, '/basic-info')

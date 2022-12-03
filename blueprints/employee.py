from flask import Blueprint
from flask_restful import Api, Resource


bp = Blueprint('employee', __name__, url_prefix='/employee')
api = Api(bp)


class EmployeeList(Resource):
    def get(self):
        return {'employees': ['John', 'Jane', 'Joe']}

    def post(self):
        return {'message': 'Employee created'}


api.add_resource(EmployeeList, '/list')

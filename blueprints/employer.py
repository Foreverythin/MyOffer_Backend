from flask import Blueprint
from flask_restful import Api, Resource, reqparse, fields, marshal_with


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


api.add_resource(EmployerList, '/list')

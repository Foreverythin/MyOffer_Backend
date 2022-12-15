from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with

import datetime

from models import Employer, Post
from exts import db, logger

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
            logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, email, 'Invalid date of establishment when updating basic info!'))
            employer.dateOfEstablishment = None
        employer.location = request.json.get('location')
        employer.staff = request.json.get('staff')
        employer.introduction = request.json.get('introduction')
        try:
            db.session.commit()
            logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, email, 'Update basic info successfully!'))
            return jsonify({'status': 200, 'msg': 'Update profile successfully!',
                            'data' :{'email': email, 'name': employer.name, 'CEO': employer.CEO, 'researchDirection': employer.researchDirection, 'dateOfEstablishment': employer.dateOfEstablishment, 'location': employer.location, 'staff': employer.staff, 'introduction': employer.introduction}})
        except Exception as e:
            db.session.rollback()
            logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, email, 'Update basic info failed because of %s!') % e)
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
        introduction = employer.introduction
        return jsonify({'status': 200, 'msg': 'Profile fetched successfully!', 'data':
            {'email': email, 'name': name, 'CEO': CEO, 'researchDirection': researchDirection, 'dateOfEstablishment': dateOfEstablishment, 'location': location, 'staff': staff, 'introduction': introduction}})


class Posts(Resource):
    @verifyEmployerToken
    def post(self):
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
        employer = Employer.query.filter_by(email=email).first()
        if employer.name is None:
            return jsonify({'status': 400, 'msg': 'Please complete your profile first!'})
        # add a new post
        title = request.json.get('title')
        salary = request.json.get('salary')
        degree = request.json.get('degree')
        label = request.json.get('label')
        tasks = request.json.get('tasks')
        requirements = request.json.get('requirements')
        inRecruitment = request.json.get('inRecruitment')
        if inRecruitment == 'true':
            inRecruitment = True
        else:
            inRecruitment = False
        post = Post(title=title, salary=salary, degree=degree, label=label, tasks=tasks, requirements=requirements, inRecruitment=inRecruitment, employerId=employer.uid)
        try:
            db.session.add(post)
            db.session.commit()
            logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, email, 'Add a new post %s successfully!') % title)
            return jsonify({'status': 200, 'msg': 'Post added successfully!'})
        except Exception as e:
            db.session.rollback()
            logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, email, 'Add a new post %s failed because of %s!') % (title, e))
            return jsonify({'status': 403, 'msg': str(e)})

    @verifyEmployerToken
    def get(self):
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
        employer = Employer.query.filter_by(email=email).first()
        posts = Post.query.filter_by(employerId=employer.uid).all()
        return jsonify({'status': 200, 'msg': 'Posts fetched successfully!', 'data': [{'ID': post.pid, 'title': post.title, 'salary': post.salary, 'degree': post.degree, 'label': post.label, 'tasks': post.tasks, 'requirements': post.requirements, 'inRecruitment': post.inRecruitment, 'receivedResumes': post.receivedResumes} for post in posts]})

    @verifyEmployerToken
    def delete(self):
        post = Post.query.filter_by(pid=request.json.get('pid')).first()
        employer = Employer.query.filter_by(uid=post.employerId).first()
        try:
            db.session.delete(post)
            db.session.commit()
            logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, employer.name, 'Delete post %s successfully!') % post.title)
            return jsonify({'status': 200, 'msg': 'Post deleted successfully!'})
        except Exception as e:
            db.session.rollback()
            logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, employer.name, 'Delete post %s failed because of %s!') % (post.title, e))
            return jsonify({'status': 403, 'msg': str(e)})


class OnePost(Resource):
    @verifyEmployerToken
    def get(self):
        pid = request.args.get('pid')
        post = Post.query.filter_by(pid=pid).first()
        return jsonify({'status': 200, 'msg': 'Posts fetched successfully!', 'data': {'ID': post.pid, 'title': post.title, 'salary': post.salary, 'degree': post.degree, 'label': post.label, 'tasks': post.tasks, 'requirements': post.requirements, 'inRecruitment': post.inRecruitment}})

    @verifyEmployerToken
    def put(self):
        pid = request.json.get('pid')
        post = Post.query.filter_by(pid=pid).first()
        post.title = request.json.get('title')
        post.salary = request.json.get('salary')
        post.degree = request.json.get('degree')
        post.label = request.json.get('label')
        post.tasks = request.json.get('tasks')
        post.requirements = request.json.get('requirements')
        inRecruitment = request.json.get('inRecruitment')
        if inRecruitment == 'true':
            post.inRecruitment = True
        else:
            post.inRecruitment = False
        try:
            db.session.commit()
            logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, post.employer.name, 'Update post %s successfully!') % post.title)
            return jsonify({'status': 200, 'msg': 'Post updated successfully!'})
        except Exception as e:
            db.session.rollback()
            logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (
                request.remote_addr, post.employer.name, 'Update post %s failed because of %s!') % (post.title, e))
            return jsonify({'status': 403, 'msg': str(e)})


api.add_resource(BasicInfo, '/basic-info')
api.add_resource(Posts, '/posts')
api.add_resource(OnePost, '/one-post')


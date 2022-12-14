import os
from authlib.jose import jwt

from flask import Blueprint, jsonify, request, send_file
from flask_mail import Message
from flask_restful import Api, Resource

from models import Employee, Post, Employer, PostEmployee
from exts import db, mail
from app import app

from config import SECRET_KEY
from utils import verifyEmployeeToken, emailByTokenStr

RESUME_UPLOAD_FOLDER = 'upload/resume/'

bp = Blueprint('employee', __name__, url_prefix='/employee')
api = Api(bp)


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

    @verifyEmployeeToken
    def delete(self):
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
        employee = Employee.query.filter_by(email=email).first()
        if employee.resume is not None:
            os.remove(RESUME_UPLOAD_FOLDER + employee.resume)
            employee.resume = None
            try:
                db.session.commit()
                return jsonify({'status': 200, 'msg': 'Delete resume successfully!'})
            except Exception as e:
                return jsonify({'status': 403, 'msg': str(e)})
        else:
            return jsonify({'status': 200, 'msg': 'No resume uploaded!'})


class DownloadResume(Resource):
    @verifyEmployeeToken
    def get(self):
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
        employee = Employee.query.filter_by(email=email).first()
        if employee.resume is not None:
            return send_file(RESUME_UPLOAD_FOLDER + employee.resume, mimetype='application/pdf')
        else:
            return jsonify({'status': 400, 'msg': 'No resume uploaded!'})


class PostList(Resource):
    @verifyEmployeeToken
    def get(self):
        title = request.args.get('title')
        city = request.args.get('city')
        salary = request.args.get('salary')
        labels = request.args.get('labels').split(',')
        viewMethod = request.args.get('viewMethod')
        postModel = Post.query.all()
        posts = []
        for post in postModel:
            employerId = post.employerId
            employer = Employer.query.filter_by(uid=employerId).first()
            if labels[0] != '' and post.label not in labels:
                continue
            if title != '' and title not in post.title:
                continue
            if city != '' and city != employer.location:
                continue
            if int(salary) > post.salary:
                continue
            if employer.name is None:
                employer_name = 'Unknown Name'
            else:
                employer_name = employer.name
            if employer.CEO is None:
                employer_CEO = 'Unknown CEO'
            else:
                employer_CEO = employer.CEO
            if employer.researchDirection is None:
                employer_researchDirection = 'Unknown research direction'
            else:
                employer_researchDirection = employer.researchDirection
            if employer.dateOfEstablishment is None:
                employer_dateOfEstablishment = 'Unknown Date'
            else:
                employer_dateOfEstablishment = employer.dateOfEstablishment.strftime('%Y-%m-%d')
            if employer.location is None:
                employer_location = 'Unknown location'
            else:
                employer_location = employer.location
            if employer.staff is None:
                employer_staff = 'Unknown staff number'
            else:
                employer_staff = employer.staff
            if employer.introduction is None:
                employer_introduction = 'No introduction'
            else:
                employer_introduction = employer.introduction
            posts.append({'post_id': post.pid, 'title': post.title, 'salary': post.salary, 'degree': post.degree, 'label': post.label, 'tasks': post.tasks, 'requirements': post.requirements, 'inRecruitment': post.inRecruitment, 'receivedResumes': post.receivedResumes,
                          'employer_id': employer.uid, 'employer_email': employer.email, 'employer_name': employer_name, 'employer_CEO': employer_CEO, 'employer_researchDirection': employer_researchDirection, 'employer_dateOfEstablishment': employer_dateOfEstablishment, 'employer_location': employer_location, 'employer_staff': employer_staff, 'employer_introduction': employer_introduction})

        if viewMethod == 'Hot Posts':
            # sort post by receivedResumes
            posts.sort(key=lambda x: x['receivedResumes'], reverse=True)
        else:
            # sort post by salary
            posts.sort(key=lambda x: x['salary'], reverse=True)

        return jsonify({'status': 200, 'msg': 'Posts fetched successfully!', 'data': {'posts': posts}})


class PostInfo(Resource):
    @verifyEmployeeToken
    def get(self):
        postID = request.args.get('postID')
        post = Post.query.filter_by(pid=postID).first()
        employerId = post.employerId
        employer = Employer.query.filter_by(uid=employerId).first()
        if employer.dateOfEstablishment is None:
            employer_dateOfEstablishment = 'Unknown Date'
        else:
            employer_dateOfEstablishment = employer.dateOfEstablishment.strftime('%Y-%m-%d')
        return jsonify({'status': 200, 'msg': 'Post fetched successfully!', 'data': {'postInfo': {'post_id': post.pid, 'title': post.title, 'salary': post.salary, 'degree': post.degree, 'label': post.label, 'tasks': post.tasks, 'requirements': post.requirements, 'inRecruitment': post.inRecruitment, 'receivedResumes': post.receivedResumes},
                                                                                     'companyInfo': {'employer_id': employer.uid, 'email': employer.email, 'name': employer.name, 'CEO': employer.CEO, 'researchDirection': employer.researchDirection, 'dateOfEstablishment': employer_dateOfEstablishment,
                                                                                              'location': employer.location, 'staff': employer.staff, 'introduction': employer.introduction}}})


class SimilarPosts(Resource):
    @verifyEmployeeToken
    def get(self):
        postID = request.args.get('postID')
        post = Post.query.filter_by(pid=postID).first()
        label = post.label
        similarPosts = Post.query.filter_by(label=label).all()
        posts = []
        for post in similarPosts:
            if post.pid != int(postID):
                posts.append({'post_id': post.pid, 'title': post.title, 'salary': post.salary, 'degree': post.degree, 'label': post.label})

        print(posts)

        return jsonify({'status': 200, 'msg': 'Similar posts fetched successfully!', 'data': {'posts': posts}})


class SendResume(Resource):
    @verifyEmployeeToken
    def post(self):
        postID = request.json.get('postID')
        post = Post.query.filter_by(pid=postID).first()
        if not post.inRecruitment:
            return jsonify({'status': 400, 'msg': 'This post is not in recruitment!'})
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)
        employee = Employee.query.filter_by(email=email).first()
        existingPostEmployee = PostEmployee.query.filter_by(pid=postID, uid=employee.uid).first()
        if existingPostEmployee is not None:
            return jsonify({'status': 400, 'msg': 'Resume already sent!'})
        if employee.resume is not None:
            employer = Employer.query.filter_by(uid=post.employerId).first()
            message = Message('New Resume', recipients=[employer.email], body='This is a resume from a person who would like to apply for the post ' + post.title + ' in your company. Please have a look!')
            with app.open_resource(RESUME_UPLOAD_FOLDER + employee.resume) as fp:
                message.attach(employee.resume, "application/pdf", fp.read())
            mail.send(message)
            post.receivedResumes += 1
            post_employee = PostEmployee(pid=postID, uid=employee.uid)
            db.session.add(post_employee)
            try:
                db.session.commit()
                return jsonify({'status': 200, 'msg': 'Resume sent successfully!'})
            except Exception as e:
                return jsonify({'status': 403, 'msg': str(e)})
        else:
            return jsonify({'status': 411, 'msg': 'No resume uploaded! Please upload your resume first!'})


api.add_resource(Profile, '/profile')
api.add_resource(Resume, '/resume')
api.add_resource(DownloadResume, '/downloadResume')
api.add_resource(PostList, '/post-list')
api.add_resource(PostInfo, '/post-info')
api.add_resource(SimilarPosts, '/similar-posts')
api.add_resource(SendResume, '/send-resume')

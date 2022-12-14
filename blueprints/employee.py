import os
from authlib.jose import jwt

from flask import Blueprint, jsonify, request, send_file
from flask_mail import Message
from flask_restful import Api, Resource

from models import Employee, Post, Employer, PostEmployee
from exts import db, mail, logger
from app import app

from config import SECRET_KEY
from utils import verifyEmployeeToken, emailByTokenStr, validTel

RESUME_UPLOAD_FOLDER = 'upload/resume/'  # the folder to store resume

bp = Blueprint('employee', __name__, url_prefix='/employee')
api = Api(bp)


class Profile(Resource):
    """
    employee profile: put, get
    """
    @verifyEmployeeToken
    def put(self):
        # get token from request header
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)  # decode token to get email
        employee = Employee.query.filter_by(email=email).first()    # get employee by email
        employee.name = request.json.get('name')  # get name from request body
        employee.gender = request.json.get('gender')  # get gender from request body
        employee.age = request.json.get('age')  # get age from request body
        employee.major = request.json.get('major')  # get major from request body
        employee.degree = request.json.get('degree')  # get degree from request body
        employee.tel = request.json.get('tel')  # get tel from request body
        if not validTel(employee.tel):      # check if tel is valid
            return jsonify({'status': 415, 'msg': 'Invalid telephone number!'})
        if int(employee.age) < 18 or int(employee.age) > 120:  # check if age is valid
            return jsonify({'status': 416, 'msg': 'Invalid age!'})
        if employee.gender == '':  # check if gender is none
            return jsonify({'status': 417, 'msg': 'Invalid gender!'})
        if employee.gender != 'male' and employee.gender != 'female':  # check if gender is valid
            return jsonify({'status': 417, 'msg': 'Invalid gender!'})
        try:
            db.session.commit()
            logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'update profile successfully'))
            return jsonify({'status': 200, 'msg': 'Update profile successfully!'})
        except Exception as e:
            db.session.rollback()
            logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'update profile failed'))
            return jsonify({'status': 403, 'msg': str(e)})

    @verifyEmployeeToken
    def get(self):
        # get token from request header
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)  # decode token to get email
        employee = Employee.query.filter_by(email=email).first()  # get employee by email
        name = employee.name  # get name from database
        gender = employee.gender  # get gender from database
        age = employee.age  # get age from database
        major = employee.major  # get major from database
        degree = employee.degree  # get degree from database
        tel = employee.tel  # get tel from database
        return jsonify({'status': 200, 'msg': 'Profile fetched successfully!', 'data':
            {'email': email, 'name': name, 'gender': gender, 'age': age, 'major': major, 'degree': degree, 'tel': tel}})


class Resume(Resource):
    """
    employee resume: post, get, delete
    """
    @verifyEmployeeToken
    def post(self):
        # get token from request header
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)  # decode token to get email
        resume = request.files.get('file')  # get resume from request body
        resumeFileName = email + '_' + resume.filename  # generate resume file name
        # delete the old resume
        employee = Employee.query.filter_by(email=email).first()  # get employee by email
        if employee.resume:  # check if resume is none
            os.remove(RESUME_UPLOAD_FOLDER + employee.resume)
        resume.save(os.path.join(RESUME_UPLOAD_FOLDER, resumeFileName))  # save resume to server
        employee.resume = resumeFileName  # update resume in database
        try:
            db.session.commit()
            logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'upload resume %s successfully') % resumeFileName)
            return jsonify({'status': 200, 'msg': 'Upload resume successfully!'})
        except Exception as e:
            db.session.rollback()
            logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'upload resume %s failed') % resumeFileName)
            return jsonify({'status': 403, 'msg': str(e)})

    @verifyEmployeeToken
    def get(self):
        # get token from request header
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)  # decode token to get email
        employee = Employee.query.filter_by(email=email).first()  # get employee by email
        if employee.resume is not None:   # check if resume is none
            _index = employee.resume.index('_')  # get the index of '_' in resume file name
            resumeFileName = employee.resume[_index + 1:]  # get resume file name
            return jsonify({'status': 200, 'msg': 'Resume fetched successfully!', 'data': {'resume': resumeFileName}})
        else:
            return jsonify({'status': 200, 'msg': 'Resume fetched successfully!', 'data': {'resume': 'No File Uploaded'}})

    @verifyEmployeeToken
    def delete(self):
        # get token from request header
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)  # decode token to get email
        employee = Employee.query.filter_by(email=email).first()  # get employee by email
        if employee.resume is not None:  # check if resume is none
            os.remove(RESUME_UPLOAD_FOLDER + employee.resume)  # delete resume from server
            employee.resume = None  # update resume in database
            try:
                db.session.commit()
                logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'delete resume successfully'))
                return jsonify({'status': 200, 'msg': 'Delete resume successfully!'})
            except Exception as e:
                db.session.rollback()
                logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'delete resume failed'))
                return jsonify({'status': 403, 'msg': str(e)})
        else:
            return jsonify({'status': 200, 'msg': 'No resume uploaded!'})


class DownloadResume(Resource):
    """
    download resume: get
    """
    @verifyEmployeeToken
    def get(self):
        # get token from request header
        tokenStr = request.headers.get('Authorization')[9:]
        email = emailByTokenStr(tokenStr)  # decode token to get email
        employee = Employee.query.filter_by(email=email).first()  # get employee by email
        if employee.resume is not None:  # check if resume is none
            logger.info('[IP] - %s, [email] - %s, [msg] - %s' % (
            request.remote_addr, email, 'download resume %s successfully' % employee.resume))
            return send_file(RESUME_UPLOAD_FOLDER + employee.resume, mimetype='application/pdf')
        else:
            logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'download resume failed - no resume uploaded'))
            return jsonify({'status': 400, 'msg': 'No resume uploaded!'})


class PostList(Resource):
    """
    post list: get
    """
    @verifyEmployeeToken
    def get(self):
        # get args from request body
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
            if labels[0] != '' and post.label not in labels:  # check if labels is empty
                continue
            if title != '' and title not in post.title:  # check if title is empty
                continue
            if city != '' and city != employer.location:  # check if city is empty
                continue
            if int(salary) > post.salary:  # check the minimum salary
                continue
            if employer.name is None:  # check if employer name is none
                employer_name = 'Unknown Name'
            else:
                employer_name = employer.name
            if employer.CEO is None:  # check if employer CEO is none
                employer_CEO = 'Unknown CEO'
            else:
                employer_CEO = employer.CEO
            if employer.researchDirection is None:  # check if employer research direction is none
                employer_researchDirection = 'Unknown research direction'
            else:
                employer_researchDirection = employer.researchDirection
            if employer.dateOfEstablishment is None:  # check if employer date of establishment is none
                employer_dateOfEstablishment = 'Unknown Date'
            else:
                employer_dateOfEstablishment = employer.dateOfEstablishment.strftime('%Y-%m-%d')
            if employer.location is None:  # check if employer location is none
                employer_location = 'Unknown location'
            else:
                employer_location = employer.location
            if employer.staff is None:  # check if employer staff is none
                employer_staff = 'Unknown staff number'
            else:
                employer_staff = employer.staff
            if employer.introduction is None:  # check if employer introduction is none
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
    """
    post info: get
    """
    @verifyEmployeeToken
    def get(self):
        postID = request.args.get('postID')  # get postID from request body
        post = Post.query.filter_by(pid=postID).first()  # get post by postID
        if post is None:  # check if post is none
            return jsonify({'status': 418, 'msg': 'No such post!'})
        employerId = post.employerId  # get employerID
        employer = Employer.query.filter_by(uid=employerId).first()  # get employer by employerID
        if employer.dateOfEstablishment is None:  # check if employer date of establishment is none
            employer_dateOfEstablishment = 'Unknown Date'
        else:
            employer_dateOfEstablishment = employer.dateOfEstablishment.strftime('%Y-%m-%d')
        return jsonify({'status': 200, 'msg': 'Post fetched successfully!', 'data': {'postInfo': {'post_id': post.pid, 'title': post.title, 'salary': post.salary, 'degree': post.degree, 'label': post.label, 'tasks': post.tasks, 'requirements': post.requirements, 'inRecruitment': post.inRecruitment, 'receivedResumes': post.receivedResumes},
                                                                                     'companyInfo': {'employer_id': employer.uid, 'email': employer.email, 'name': employer.name, 'CEO': employer.CEO, 'researchDirection': employer.researchDirection, 'dateOfEstablishment': employer_dateOfEstablishment,
                                                                                              'location': employer.location, 'staff': employer.staff, 'introduction': employer.introduction}}})


class SimilarPosts(Resource):
    """
    similar posts: get
    """
    @verifyEmployeeToken
    def get(self):
        postID = request.args.get('postID')  # get postID from request body
        post = Post.query.filter_by(pid=postID).first()  # get post by postID
        if post is None:  # check if post is none
            return jsonify({'status': 418, 'msg': 'No such post!'})
        label = post.label
        similarPosts = Post.query.filter_by(label=label).all()  # get similar posts by label
        posts = []
        for post in similarPosts:
            if post.pid != int(postID):
                posts.append({'post_id': post.pid, 'title': post.title, 'salary': post.salary, 'degree': post.degree, 'label': post.label})

        return jsonify({'status': 200, 'msg': 'Similar posts fetched successfully!', 'data': {'posts': posts}})


class SendResume(Resource):
    """
    send resume from an employee: post
    """
    @verifyEmployeeToken
    def post(self):
        postID = request.json.get('postID')  # get postID from request body
        post = Post.query.filter_by(pid=postID).first()  # get post by postID
        if post is None:  # check if post is none
            return jsonify({'status': 418, 'msg': 'No such post!'})
        if not post.inRecruitment:  # check if post is in recruitment
            return jsonify({'status': 400, 'msg': 'This post is not in recruitment!'})
        tokenStr = request.headers.get('Authorization')[9:]  # get token from request header
        email = emailByTokenStr(tokenStr)  # get email by token
        employee = Employee.query.filter_by(email=email).first()  # get employee by email
        existingPostEmployee = PostEmployee.query.filter_by(pid=postID, uid=employee.uid).first()  # get postEmployee by postID and employeeID
        if existingPostEmployee is not None:  # check if postEmployee is none
            logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'Resume sent failed because the resume has already sent before!'))
            return jsonify({'status': 400, 'msg': 'Resume already sent!'})
        if employee.resume is not None:  # check if employee resume is none
            employer = Employer.query.filter_by(uid=post.employerId).first()
            message = Message('New Resume', recipients=[employer.email], body='This is a resume from a person who would like to apply for the post ' + post.title + ' in your company. Please have a look!')
            with app.open_resource(RESUME_UPLOAD_FOLDER + employee.resume) as fp:
                message.attach(employee.resume, "application/pdf", fp.read())
            mail.send(message)  # send email
            post.receivedResumes += 1  # add receivedResumes
            post_employee = PostEmployee(pid=postID, uid=employee.uid)  # create postEmployee
            db.session.add(post_employee)
            try:
                db.session.commit()
                logger.info(
                    '[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'Resume sent successfully!'))
                return jsonify({'status': 200, 'msg': 'Resume sent successfully!'})
            except Exception as e:
                db.session.rollback()
                logger.error('[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'Resume sent failed because of %s!' % e))
                return jsonify({'status': 403, 'msg': str(e)})
        else:
            logger.warning('[IP] - %s, [email] - %s, [msg] - %s' % (request.remote_addr, email, 'Resume sent failed because the resume is not uploaded!'))
            return jsonify({'status': 411, 'msg': 'No resume uploaded! Please upload your resume first!'})


#############################################  API Defined  ###############################################
api.add_resource(Profile, '/profile')
api.add_resource(Resume, '/resume')
api.add_resource(DownloadResume, '/downloadResume')
api.add_resource(PostList, '/post-list')
api.add_resource(PostInfo, '/post-info')
api.add_resource(SimilarPosts, '/similar-posts')
api.add_resource(SendResume, '/send-resume')
###########################################################################################################

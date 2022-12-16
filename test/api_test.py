import unittest
import json
import forms

from app import app
from models import Employee, Employer, Post, db

from utils import generateToken


class TestEmployeeLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_wrong_password(self):
        emails = ['mn20pl@leeds.ac.uk', 'pangyuli92@gmail.com']
        passwords = ['123456', 'abcdefg', 'abcd1234', '*&^%$#@!', '123.abc']
        for email in emails:
            for password in passwords:
                response = self.app.post('/login/employee', data=json.dumps({'email': email, 'password': password}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 401)
                msg = resp_dict['msg']
                self.assertEqual(msg, 'Invalid email or password!')

    def test_invalid_password(self):
        emails = ['mn20pl@leeds.ac.uk', 'pangyuli92@gmail.com']
        passwords = ['', '12345', '*.&', '00000', '     ', '1 2 a', 'a_very_long_long_password']
        for email in emails:
            for password in passwords:
                response = self.app.post('/login/employee', data=json.dumps({'email': email, 'password': password}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 402)

    def test_unregistered_email(self):
        emails = ['mn20kk@leeds.ac.uk', '123451234@qq.com', 'pangyu@gmail.com', 'swjtu@163.com']
        passwords = ['123456', 'abcdef', '123abc', '123.abc', '*&^%$#@!']
        for email in emails:
            for password in passwords:
                response = self.app.post('/login/employee', data=json.dumps({'email': email, 'password': password}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 400)
                msg = resp_dict['msg']
                self.assertEqual(msg, 'Account does not exist!')

    def test_invaild_email(self):
        emails = ['', '123451234', 'pangyu', 'swjtu@163', 'swjtu@163.', '*&^%$#@!', '      ']
        passwords = ['123456', 'abcdef', '123abc', '123.abc', '*&^%$#@!']
        for email in emails:
            for password in passwords:
                response = self.app.post('/login/employee', data=json.dumps({'email': email, 'password': password}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 402)

    def test_employer_email(self):
        emails = ['mn20xy@leeds.ac.uk', '198013594@qq.com', '1419360585@qq.com']
        password = 'lpy..2002'
        for email in emails:
            response = self.app.post('/login/employee', data=json.dumps({'email': email, 'password': password}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 400)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Account does not exist!')

    def test_right_password(self):
        emails = ['mn20pl@leeds.ac.uk', 'pangyuli92@gmail.com']
        password = 'lpy..2002'
        for email in emails:
            response = self.app.post('/login/employee', data=json.dumps({'email': email, 'password': password}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 200)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Successfully logged in!')

    def tearDown(self):
        with app.app_context():
            employee1 = Employee.query.filter_by(email='mn20pl@leeds.ac.uk').first()
            employee2 = Employee.query.filter_by(email='pangyuli92@gmail.com').first()
            employee1.logged = False
            employee2.logged = False


class TestEmployerLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_wrong_password(self):
        emails = ['mn20xy@leeds.ac.uk', '198013594@qq.com', '1419360585@qq.com']
        passwords = ['123456', 'abcdefg', 'abcd1234', '*&^%$#@!', '123.abc']
        for email in emails:
            for password in passwords:
                response = self.app.post('/login/employer', data=json.dumps({'email': email, 'password': password}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 401)
                msg = resp_dict['msg']
                self.assertEqual(msg, 'Invalid email or password!')

    def test_invalid_password(self):
        emails = ['mn20xy@leeds.ac.uk', '198013594@qq.com', '1419360585@qq.com']
        passwords = ['', '12345', '*.&', '00000', '     ', '1 2 a', 'a_very_long_long_password']
        for email in emails:
            for password in passwords:
                response = self.app.post('/login/employer', data=json.dumps({'email': email, 'password': password}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 402)

    def test_unregistered_email(self):
        emails = ['mn20kk@leeds.ac.uk', '123451234@qq.com', 'pangyu@gmail.com', 'swjtu@163.com']
        passwords = ['123456', 'abcdef', '123abc', '123.abc', '*&^%$#@!']
        for email in emails:
            for password in passwords:
                response = self.app.post('/login/employer', data=json.dumps({'email': email, 'password': password}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 400)
                msg = resp_dict['msg']
                self.assertEqual(msg, 'Account does not exist!')

    def test_invaild_email(self):
        emails = ['', '123451234', 'pangyu', 'swjtu@163', 'swjtu@163.', '*&^%$#@!', '      ']
        passwords = ['123456', 'abcdef', '123abc', '123.abc', '*&^%$#@!']
        for email in emails:
            for password in passwords:
                response = self.app.post('/login/employer', data=json.dumps({'email': email, 'password': password}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 402)

    def test_employee_email(self):
        emails = ['mn20pl@leeds.ac.uk', 'pangyuli92@gmail.com']
        password = 'lpy..2002'
        for email in emails:
            response = self.app.post('/login/employer', data=json.dumps({'email': email, 'password': password}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 400)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Account does not exist!')

    def test_right_password(self):
        emails = ['mn20xy@leeds.ac.uk', '198013594@qq.com', '1419360585@qq.com']
        password = 'lpy..2002'
        for email in emails:
            response = self.app.post('/login/employer', data=json.dumps({'email': email, 'password': password}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 200)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Successfully logged in!')

    def tearDown(self):
        with app.app_context():
            employer1 = Employer.query.filter_by(email='mn20xy@leeds.ac.uk').first()
            employer2 = Employer.query.filter_by(email='198013594@qq.com').first()
            employer3 = Employer.query.filter_by(email='1419360585@qq.com').first()
            employer1.logged = False
            employer2.logged = False
            employer3.logged = False


# class TestEmployeeRegister(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#         self.app.testing = True
#
#     def test_invalid_email(self):
#         emails = ['', '123451234', 'pangyu', 'swjtu@163', 'swjtu@163.', '*&^%$#@!', '      ']
#         passwords = ['123456', 'abcdef', '123abc', '123.abc', '*&^%$#@!']
#         for email in emails:
#             for password in passwords:
#                 response = self.app.post('/register/employee', data=json.dumps({'email': email, 'password': password}),
#                                          content_type='application/json')
#                 resp_json = response.data
#                 resp_dict = json.loads(resp_json)
#                 self.assertIn('message', resp_dict)
#
#     def test_invalid_password(self):
#         emails = ['mn20pp@leeds.ac.uk', '1510397455@qq.com', 'pangyuli@gmail.com']
#         passwords = ['', '12345', '*.&', '00000', '     ', '1 2 a', 'a_very_long_long_password']
#         for email in emails:
#             for password in passwords:
#                 response = self.app.post('/register/employee', data=json.dumps({'email': email, 'password': password}),
#                                          content_type='application/json')
#                 resp_json = response.data
#                 resp_dict = json.loads(resp_json)
#                 self.assertIn('message', resp_dict)
#
#     def test_registered_email(self):
#         emails = ['mn20pl@leeds.ac.uk', 'pangyuli92@gmail.com', 'mn20xy@leeds.ac.uk', '198013594@qq.com', '1419360585@qq.com']
#         password = 'lpy..2002'
#         for email in emails:
#             response = self.app.post('/register/employee', data=json.dumps({'email': email, 'password': password}),
#                                      content_type='application/json')
#             resp_json = response.data
#             resp_dict = json.loads(resp_json)
#             self.assertIn('message', resp_dict)
#
#     def test_valid_email_password(self):
#         emails = ['mn20pp@leeds.ac.uk', '1510397455@qq.com', 'pangyuli@gmail.com']
#         passwords = ['lpy..2002', 'abcdef', '123abc']
#         for email in emails:
#             for password in passwords:
#                 response = self.app.post('/register/employee', data=json.dumps({'email': email, 'password': password}),
#                                          content_type='application/json')
#                 resp_json = response.data
#                 resp_dict = json.loads(resp_json)
#                 self.assertIn('status', resp_dict)
#                 status = resp_dict['status']
#                 self.assertEqual(status, 200)
#                 msg = resp_dict['msg']
#                 self.assertEqual(msg, 'The user registered successfully as an employee!')


class TestGetCaptcha(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_valid_email_get_captcha(self):
        # emails already have been registered
        emails = ['mn20pl@leeds.ac.uk', 'pangyuli92@gmail.com', 'mn20xy@leeds.ac.uk', '198013594@qq.com']
        for email in emails:
            response = self.app.get('/captcha?email=' + email, content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 405)

        # emails not registered
        emails = ['1647970332@qq.com', '2083097585@qq.com']
        for email in emails:
            response = self.app.get('/captcha?email=' + email, content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 200)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Captcha has been sent to your email address!')


class TestLogout(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            loggedEmployee = Employee.query.filter_by(email='mn20pl@leeds.ac.uk').first()
            loggedEmployee.logged = True
            self.loggedEmployeeToken = str('employee:') + generateToken(loggedEmployee.email)
            loggedEmployer = Employer.query.filter_by(email='mn20xy@leeds.ac.uk').first()
            loggedEmployer.logged = True
            self.loggedEmployerToken = str('employer:') + generateToken(loggedEmployer.email)
            notLoggedEmployee = Employee.query.filter_by(email='pangyuli92@gmail.com').first()
            notLoggedEmployee.logged = False
            self.notLoggedEmployeeToken = str('employee:') + generateToken(notLoggedEmployee.email)
            notLoggedEmployer = Employer.query.filter_by(email='198013594@qq.com').first()
            notLoggedEmployer.logged = False
            self.notLoggedEmployerToken = str('employer:') + generateToken(notLoggedEmployer.email)

    def test_not_logged_in(self):
        # not logged - employee
        response = self.app.get('/logout/employee', headers={'authorization': self.notLoggedEmployeeToken},
                                content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 200)

        # not logged - employer
        response = self.app.get('/logout/employer', headers={'authorization': self.notLoggedEmployerToken},
                                content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 200)

    def test_logged_in(self):
        # logged - employee
        response = self.app.get('/logout/employee', headers={'authorization': self.loggedEmployeeToken},
                                content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 200)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Successfully logged out!')

        # logged - employer
        response = self.app.get('/logout/employer', headers={'authorization': self.loggedEmployerToken},
                                content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 200)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Successfully logged out!')

    def tearDown(self):
        with app.app_context():
            loggedEmployee = Employee.query.filter_by(email='mn20pl@leeds.ac.uk').first()
            loggedEmployee.logged = False
            loggedEmployer = Employer.query.filter_by(email='mn20xy@leeds.ac.uk').first()
            loggedEmployer.logged = False


if __name__ == '__main__':
    unittest.main()

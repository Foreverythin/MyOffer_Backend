import unittest
import json

from app import app
from models import Employee, Employer, Post, db, Captcha


class TestEmployeeLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.loggedToken = []

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
            self.loggedToken.append(resp_dict['token'])

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
        self.loggedToken = []

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
            self.loggedToken.append(resp_dict['token'])

    def tearDown(self):
        with app.app_context():
            employer1 = Employer.query.filter_by(email='mn20xy@leeds.ac.uk').first()
            employer2 = Employer.query.filter_by(email='198013594@qq.com').first()
            employer3 = Employer.query.filter_by(email='1419360585@qq.com').first()
            employer1.logged = False
            employer2.logged = False
            employer3.logged = False


class TestEmployeeRegister(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()
        self.app.testing = True

    def test_invalid_email(self):
        emails = ['', '123451234', 'pangyu', 'swjtu@163', 'swjtu@163.', '*&^%$#@!', '      ']
        passwords = ['123456', 'abcdef', '123abc', '123.abc', '*&^%$#@!']
        for email in emails:
            for password in passwords:
                response = self.app.post('/register/employee', data=json.dumps(
                    {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': '1234'}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 402)

    def test_registered_email(self):
        # employee
        emails = ['mn20pl@leeds.ac.uk', 'pangyuli92@gmail.com']
        password = 'lpy..2002'
        for email in emails:
            response = self.app.post('/register/employee', data=json.dumps(
                {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': '1234'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 404)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Failed to register! Email already registered as an identity of an employee')

        # employer
        emails = ['mn20xy@leeds.ac.uk', '198013594@qq.com']
        password = 'lpy..2002'
        for email in emails:
            response = self.app.post('/register/employee', data=json.dumps(
                {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': '1234'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 404)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Failed to register! Email already registered as an identity of an employer')

    def test_invalid_password(self):
        emails = ['2083097585@qq.com', '1647970332@qq.com']
        passwords = ['', '12345', 'abef', '123ac', '1.abc', 'a_very_long_password']
        for email in emails:
            for password in passwords:
                response = self.app.post('/register/employee', data=json.dumps(
                    {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': '1234'}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 402)
                msg = resp_dict['msg']
                self.assertEqual(msg, 'The length of password should be between 6 and 18!')

    def test_password_not_match(self):
        emails = ['2083097585@qq.com', '1647970332@qq.com']
        password = 'lpy..2002'
        confirmedPassword = 'lpy..2003'
        for email in emails:
            response = self.app.post('/register/employee', data=json.dumps(
                {'email': email, 'password': password, 'confirmedPassword': confirmedPassword, 'captcha': '1234'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 402)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'The two passwords are not the same!')

    def invalid_captcha(self):
        emails = ['2083097585@qq.com', '1647970332@qq.com']
        password = 'lpy..2002'
        for email in emails:
            response = self.app.post('/register/employee', data=json.dumps(
                {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': '1000'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 402)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Invalid captcha!')

    def test_success(self):
        emails = ['2083097585@qq.com', '1647970332@qq.com']
        password = 'lpy..2002'
        for email in emails:
            with app.app_context():
                self.app.get('/captcha')
                captcha = Captcha.query.filter_by(email=email).first()
                # wait for 2 second to ensure the captcha is valid
                response = self.app.post('/register/employee', data=json.dumps(
                    {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': captcha.captcha}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 200)
                msg = resp_dict['msg']
                self.assertEqual(msg, 'Successfully registered!')

    def tearDown(self) -> None:
        emails = ['2083097585@qq.com', '1647970332@qq.com']
        for email in emails:
            with app.app_context():
                employee = Employee.query.filter_by(email=email).first()
                if employee:
                    db.session.delete(employee)
                    db.session.commit()


class TestEmployerRegister(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()
        self.app.testing = True

    def test_invalid_email(self):
        emails = ['', '123451234', 'pangyu', 'swjtu@163', 'swjtu@163.', '*&^%$#@!', '      ']
        passwords = ['123456', 'abcdef', '123abc', '123.abc', '*&^%$#@!']
        for email in emails:
            for password in passwords:
                response = self.app.post('/register/employer', data=json.dumps(
                    {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': '1234'}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 402)

    def test_registered_email(self):
        # employer
        emails = ['mn20xy@leeds.ac.uk', '198013594@qq.com']
        password = 'lpy..2002'
        for email in emails:
            response = self.app.post('/register/employer', data=json.dumps(
                {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': '1234'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 404)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Failed to register! Email already registered as an identity of an employer')

    def test_invalid_password(self):
        emails = ['mn20xy@leeds.ac.uk', '198013594@qq.com']
        passwords = ['', '12345', 'abef', '123ac', '1.abc', 'a_very_long_password']
        for email in emails:
            for password in passwords:
                response = self.app.post('/register/employer', data=json.dumps(
                    {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': '1234'}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 402)
                msg = resp_dict['msg']
                self.assertEqual(msg, 'The length of password should be between 6 and 18!')

    def test_password_not_match(self):
        emails = ['2083097585@qq.com', '1647970332@qq.com']
        password = 'lpy..2002'
        confirmedPassword = 'lpy..2003'
        for email in emails:
            response = self.app.post('/register/employer', data=json.dumps(
                {'email': email, 'password': password, 'confirmedPassword': confirmedPassword, 'captcha': '1234'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 402)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'The two passwords are not the same!')

    def invalid_captcha(self):
        emails = ['2083097585@qq.com', '1647970332@qq.com']
        password = 'lpy..2002'
        for email in emails:
            response = self.app.post('/register/employer', data=json.dumps(
                {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': '1000'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 402)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Invalid captcha!')

    def test_success(self):
        emails = ['2083097585@qq.com', '1647970332@qq.com']
        password = 'lpy..2002'
        for email in emails:
            with app.app_context():
                self.app.get('/captcha')
                captcha = Captcha.query.filter_by(email=email).first()
                # wait for 2 second to ensure the captcha is valid
                response = self.app.post('/register/employer', data=json.dumps(
                    {'email': email, 'password': password, 'confirmedPassword': password, 'captcha': captcha.captcha}),
                                         content_type='application/json')
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 200)
                msg = resp_dict['msg']
                self.assertEqual(msg, 'Successfully registered!')

    def tearDown(self) -> None:
        emails = ['2083097585@qq.com', '1647970332@qq.com']
        for email in emails:
            with app.app_context():
                employer = Employer.query.filter_by(email=email).first()
                if employer:
                    db.session.delete(employer)
                    db.session.commit()


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
            # loggedEmployee = Employee.query.filter_by(email='mn20pl@leeds.ac.uk').first()
            # loggedEmployee.logged = True
            # self.loggedEmployeeToken = str('employee:') + generateToken(loggedEmployee.email)
            # loggedEmployer = Employer.query.filter_by(email='mn20xy@leeds.ac.uk').first()
            # loggedEmployer.logged = True
            # self.loggedEmployerToken = str('employer:') + generateToken(loggedEmployer.email)
            # notLoggedEmployee = Employee.query.filter_by(email='pangyuli92@gmail.com').first()
            # notLoggedEmployee.logged = False
            # self.notLoggedEmployeeToken = str('employee:') + generateToken(notLoggedEmployee.email)
            # notLoggedEmployer = Employer.query.filter_by(email='198013594@qq.com').first()
            # notLoggedEmployer.logged = False
            # self.notLoggedEmployerToken = str('employer:') + generateToken(notLoggedEmployer.email)
            response = self.app.post('/login/employee', data=json.dumps({'email': 'mn20pl@leeds.ac.uk', 'password': 'lpy..2002'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 200)
            self.loggedEmployeeToken = resp_dict['token']
            self.notLoggedEmployeeToken = resp_dict['token']+'1'

            response = self.app.post('/login/employer', data=json.dumps({'email': 'mn20xy@leeds.ac.uk', 'password': 'lpy..2002'}),
                                        content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 200)
            self.loggedEmployerToken = resp_dict['token']
            self.notLoggedEmployerToken = resp_dict['token'] + '1'

    def test_not_logged_in(self):
        # not logged - employee
        response = self.app.get('/logout/employee', headers={'authorization': self.notLoggedEmployeeToken},
                                content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 409)

        # not logged - employer
        response = self.app.get('/logout/employer', headers={'authorization': self.notLoggedEmployerToken},
                                content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 409)

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
            # loggedEmployee = Employee.query.filter_by(email='mn20pl@leeds.ac.uk').first()
            # loggedEmployee.logged = False
            # loggedEmployer = Employer.query.filter_by(email='mn20xy@leeds.ac.uk').first()
            # loggedEmployer.logged = False
            self.app.get('/logout/employee', headers={'Authorization': self.loggedEmployeeToken},
                         content_type='application/json')
            self.app.get('/logout/employer', headers={'Authorization': self.loggedEmployerToken},
                            content_type='application/json')


class TestChangePassword(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            response = self.app.post('/login/employee',
                                     data=json.dumps({'email': 'mn20pl@leeds.ac.uk', 'password': 'lpy..2002'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 200)
            self.loggedEmployeeToken = resp_dict['token']
            self.notLoggedEmployeeToken = resp_dict['token'] + '1'

            response = self.app.post('/login/employer',
                                     data=json.dumps({'email': 'mn20xy@leeds.ac.uk', 'password': 'lpy..2002'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 200)
            self.loggedEmployerToken = resp_dict['token']
            self.notLoggedEmployerToken = resp_dict['token'] + '1'
            # loggedEmployee = Employee.query.filter_by(email='mn20pl@leeds.ac.uk').first()
            # loggedEmployee.logged = True
            # self.loggedEmployeeToken = str('employee:') + generateToken(loggedEmployee.email)
            # loggedEmployer = Employer.query.filter_by(email='mn20xy@leeds.ac.uk').first()
            # loggedEmployer.logged = True
            # self.loggedEmployerToken = str('employer:') + generateToken(loggedEmployer.email)
            # notLoggedEmployee = Employee.query.filter_by(email='pangyuli92@gmail.com').first()
            # notLoggedEmployee.logged = False
            # self.notLoggedEmployeeToken = str('employee:') + generateToken(notLoggedEmployee.email)
            # notLoggedEmployer = Employer.query.filter_by(email='198013594@qq.com').first()
            # notLoggedEmployer.logged = False
            # self.notLoggedEmployerToken = str('employer:') + generateToken(notLoggedEmployer.email)

    def test_not_logged_in(self):
        response = self.app.put('/changePassword/employer', data=json.dumps({'captcha': 'aaaa', 'password': 'asdvfgh'}),
                                headers={'Authorization': self.notLoggedEmployerToken})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 409)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Please log in first!')

    def test_invalid_captcha(self):
        response = self.app.put('/changePassword/employer', data=json.dumps({'captcha': 'aaaa', 'password': 'asdvfgh'}),
                                headers={'Authorization': self.loggedEmployerToken}, content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 404)

        response = self.app.put('/changePassword/employee', data=json.dumps({'captcha': 'aaaa', 'password': 'asdvfgh'}),
                                headers={'Authorization': self.loggedEmployeeToken}, content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 404)
        self.assertIn('msg', resp_dict)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Invalid captcha!')

    def test_invalid_password(self):
        passwords = ['', '12345', '*.&', '00000', '     ', '1 2 a', 'a_very_long_long_password']
        for password in passwords:
            response = self.app.put('/changePassword/employer',
                                    data=json.dumps({'captcha': 'aaaa', 'password': password}),
                                    headers={'Authorization': self.loggedEmployerToken}, content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 404)

            response = self.app.put('/changePassword/employee',
                                    data=json.dumps({'captcha': 'aaaa', 'password': password}),
                                    headers={'Authorization': self.loggedEmployeeToken},
                                    content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 404)
            self.assertIn('msg', resp_dict)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Invalid captcha!')

    def tearDown(self) -> None:
        with app.app_context():
            # loggedEmployee = Employee.query.filter_by(email='mn20pl@leeds.ac.uk').first()
            # loggedEmployee.logged = False
            # loggedEmployer = Employer.query.filter_by(email='mn20xy@leeds.ac.uk').first()
            # loggedEmployer.logged = False
            self.app.get('/logout/employee', headers={'Authorization': self.loggedEmployeeToken}, content_type='application/json')
            self.app.get('/logout/employer', headers={'Authorization': self.loggedEmployerToken}, content_type='application/json')


class TestChangeEmployeeProfile(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            response = self.app.post('/login/employee',
                                     data=json.dumps({'email': 'mn20pl@leeds.ac.uk', 'password': 'lpy..2002'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.loggedEmployeeToken = resp_dict['token']

    def test_valid(self):
        data1 = {'name': 'pangyu', 'gender': 'male', 'age': 20, 'major': 'EE',
                 'degree': 'bachelor', 'tel': '18031068094'}
        data2 = {'name': 'pangyu', 'gender': 'female', 'age': 30, 'major': 'CS',
                 'degree': 'bachelor', 'tel': '18031068094'}
        data3 = {'name': 'pangyu', 'gender': 'male', 'age': 40, 'major': 'ME',
                 'degree': 'master', 'tel': '13281218209'}
        data4 = {'name': 'pangyu', 'gender': 'male', 'age': 20, 'major': 'CE',
                 'degree': 'doctor', 'tel': '13281218209'}
        datas = [data1, data2, data3, data4]
        for data in datas:
            response = self.app.put('/employee/profile', data=json.dumps(data), content_type='application/json',
                                    headers={'Authorization': self.loggedEmployeeToken})
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 200)
            self.assertIn('msg', resp_dict)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Update profile successfully!')

    def test_invalid_tel(self):
        # invalid tel
        data1 = {'name': 'pangyu', 'gender': 'male', 'age': '18', 'major': 'EE',
                 'degree': 'bachelor', 'tel': 'asdfasdf'}
        data2 = {'name': 'pangyu', 'gender': 'female', 'age': '20', 'major': 'EE',
                 'degree': 'bachelor', 'tel': '1803106809'}
        data3 = {'name': 'pangyu', 'gender': 'female', 'age': '20', 'major': 'EE',
                 'degree': 'bachelor', 'tel': 'asdf1243'}
        data4 = {'name': 'pangyu', 'gender': 'female', 'age': '20', 'major': 'EE',
                 'degree': 'bachelor', 'tel': 'asdf12434ui357984'}
        invalidTels = [data1, data2, data3, data4]
        for data in invalidTels:
            response = self.app.put('/employee/profile', data=json.dumps(data), content_type='application/json',
                                    headers={'Authorization': self.loggedEmployeeToken})
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 415)
            self.assertIn('msg', resp_dict)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Invalid telephone number!')

    def test_invalid_age(self):
        # invalid age
        data1 = {'name': 'pangyu', 'gender': 'male', 'age': '-3', 'major': 'EE',
                 'degree': 'bachelor', 'tel': '18031068093'}
        data2 = {'name': 'pangyu', 'gender': 'female', 'age': '0', 'major': 'EE',
                 'degree': 'bachelor', 'tel': '18031068093'}
        data3 = {'name': 'pangyu', 'gender': 'female', 'age': '121', 'major': 'EE',
                 'degree': 'bachelor', 'tel': '18031068093'}
        data4 = {'name': 'pangyu', 'gender': 'female', 'age': '200', 'major': 'EE',
                 'degree': 'bachelor', 'tel': '18031068093'}
        invalidAges = [data1, data2, data3, data4]
        for data in invalidAges:
            response = self.app.put('/employee/profile', data=json.dumps(data), content_type='application/json',
                                    headers={'Authorization': self.loggedEmployeeToken})
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 416)
            self.assertIn('msg', resp_dict)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Invalid age!')

    def test_invalid_gender(self):
        data1 = {'name': 'pangyu', 'gender': '', 'age': '18', 'major': 'EE',
                 'degree': 'bachelor', 'tel': '18031068093'}
        data2 = {'name': 'pangyu', 'gender': 'mal', 'age': '20', 'major': 'EE',
                 'degree': 'bachelor', 'tel': '18031068093'}
        data3 = {'name': 'pangyu', 'gender': 'femall', 'age': '21', 'major': 'EE',
                 'degree': 'bachelor', 'tel': '18031068093'}
        invalidGenders = [data1, data2, data3]
        for data in invalidGenders:
            response = self.app.put('/employee/profile', data=json.dumps(data), content_type='application/json',
                                    headers={'Authorization': self.loggedEmployeeToken})
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 417)
            self.assertIn('msg', resp_dict)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Invalid gender!')

    def tearDown(self) -> None:
        self.app.get('/employee/logout', headers={'Authorization': self.loggedEmployeeToken})


class TestResume(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            response1 = self.app.post('/login/employee',
                                      data=json.dumps({'email': 'mn20pl@leeds.ac.uk', 'password': 'lpy..2002'}),
                                      content_type='application/json')
            resp_json1 = response1.data
            resp_dict1 = json.loads(resp_json1)
            self.loggedEmployeeToken1 = resp_dict1['token']

            response2 = self.app.post('/login/employee',
                                      data=json.dumps({'email': 'pangyuli92@gmail.com', 'password': 'lpy..2002'}),
                                      content_type='application/json')
            resp_json2 = response2.data
            resp_dict2 = json.loads(resp_json2)
            self.loggedEmployeeToken2 = resp_dict2['token']

    def test_get_resume(self):
        # has resume
        response = self.app.get('/employee/resume', headers={'Authorization': self.loggedEmployeeToken1})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 200)
        self.assertIn('msg', resp_dict)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Resume fetched successfully!')

        # no resume
        response = self.app.get('/employee/resume', headers={'Authorization': self.loggedEmployeeToken2})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 200)
        self.assertIn('msg', resp_dict)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Resume fetched successfully!')

    def test_download_resume(self):
        # has resume
        response = self.app.get('/employee/downloadResume', headers={'Authorization': self.loggedEmployeeToken2})
        # application/pdf
        self.assertEqual(response.content_type, 'application/pdf')
        # close the file
        response.close()

        # no resume
        response = self.app.get('/employee/downloadResume', headers={'Authorization': self.loggedEmployeeToken1})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 400)
        self.assertIn('msg', resp_dict)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'No resume uploaded!')

    def tearDown(self) -> None:
        self.app.get('/logout/employee', headers={'Authorization': self.loggedEmployeeToken1})
        self.app.get('/logout/employee', headers={'Authorization': self.loggedEmployeeToken2})


class TestPostInfo(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            response = self.app.post('/login/employee',
                                     data=json.dumps({'email': 'mn20pl@leeds.ac.uk', 'password': 'lpy..2002'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.loggedEmployeeToken = resp_dict['token']

    def test_invalid_post_id(self):
        ids = [0, -1, -5, 500]
        for id in ids:
            response = self.app.get('/employee/post-info?postID=' + str(id),
                                    headers={'Authorization': self.loggedEmployeeToken})
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 418)
            self.assertIn('msg', resp_dict)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'No such post!')

    def test_valid_post_id(self):
        ids = [1, 3, 4]
        for id in ids:
            response = self.app.get('/employee/post-info?postID=' + str(id),
                                    headers={'Authorization': self.loggedEmployeeToken})
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 200)
            self.assertIn('msg', resp_dict)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Post fetched successfully!')

    def tearDown(self) -> None:
        with app.app_context():
            self.app.get('/logout/employee', headers={'Authorization': self.loggedEmployeeToken})


class TestSimilarPosts(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            response = self.app.post('/login/employee',
                                     data=json.dumps({'email': 'mn20pl@leeds.ac.uk', 'password': 'lpy..2002'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.loggedEmployeeToken = resp_dict['token']

    def test_invalid_post_id(self):
        ids = [0, -1, -5, 500]
        for id in ids:
            response = self.app.get('/employee/similar-posts?postID=' + str(id),
                                    headers={'Authorization': self.loggedEmployeeToken})
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 418)
            self.assertIn('msg', resp_dict)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'No such post!')

    def test_valid_post_id(self):
        ids = [1, 3, 4]
        for id in ids:
            response = self.app.get('/employee/similar-posts?postID=' + str(id),
                                    headers={'Authorization': self.loggedEmployeeToken})
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 200)
            self.assertIn('msg', resp_dict)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'Similar posts fetched successfully!')

    def tearDown(self) -> None:
        with app.app_context():
            self.app.get('/logout/employee', headers={'Authorization': self.loggedEmployeeToken})


class TestSendResume(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        with app.app_context():
            response = self.app.post('/login/employee',
                                     data=json.dumps({'email': 'mn20pl@leeds.ac.uk', 'password': 'lpy..2002'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.loggedEmployeeToken = resp_dict['token']

    def test_invalid_post_id(self):
        ids = [0, -1, -5, 500]
        for id in ids:
            response = self.app.post('/employee/send-resume', data=json.dumps({'postID': str(id)}),
                                     headers={'Authorization': self.loggedEmployeeToken},
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.assertIn('status', resp_dict)
            status = resp_dict['status']
            self.assertEqual(status, 418)
            self.assertIn('msg', resp_dict)
            msg = resp_dict['msg']
            self.assertEqual(msg, 'No such post!')

    def test_out_of_recruitment_post(self):
        response = self.app.post('/employee/send-resume', data=json.dumps({'postID': '3'}),
                                 headers={'Authorization': self.loggedEmployeeToken}, content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 400)
        self.assertIn('msg', resp_dict)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'This post is not in recruitment!')

    def test_resume_has_been_sent(self):
        response = self.app.post('/employee/send-resume', data=json.dumps({'postID': '4'}),
                                 headers={'Authorization': self.loggedEmployeeToken}, content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 411)
        self.assertIn('msg', resp_dict)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'No resume uploaded! Please upload your resume first!')

    def tearDown(self) -> None:
        with app.app_context():
            self.app.get('/logout/employee', headers={'Authorization': self.loggedEmployeeToken})


class TestEmployerBasicInfo(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            response = self.app.post('/login/employer',
                                     data=json.dumps({'email': 'mn20xy@leeds.ac.uk', 'password': 'lpy..2002'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.loggedEmployeeToken = resp_dict['token']

    def test_not_logged_in(self):
        response = self.app.get('/employer/basic-info', headers={'Authorization': self.loggedEmployeeToken + '1'})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 409)
        self.assertIn('msg', resp_dict)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Please log in first!')

    def test_logged_in(self):
        response = self.app.get('/employer/basic-info', headers={'Authorization': self.loggedEmployeeToken})
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 200)
        self.assertIn('msg', resp_dict)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Profile fetched successfully!')

    def tearDown(self) -> None:
        with app.app_context():
            self.app.get('/logout/employer', headers={'Authorization': self.loggedEmployeeToken})


class TestEmployerPosts(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            response = self.app.post('/login/employer',
                                     data=json.dumps({'email': 'mn20xy@leeds.ac.uk', 'password': 'lpy..2002'}),
                                     content_type='application/json')
            resp_json = response.data
            resp_dict = json.loads(resp_json)
            self.loggedEmployerToken = resp_dict['token']

    def test_new_post(self):
        response = self.app.post('/employer/posts', data=json.dumps(
            {'title': 'unittest', 'salary': 3500, 'degree': 'Bachelor', 'label': 'C#', 'tasks': 'test',
             'requirements': 'test', 'inRecruitment': True}), headers={'Authorization': self.loggedEmployerToken},
                                 content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 200)
        self.assertIn('msg', resp_dict)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Post added successfully!')

    def test_edit_post(self):
        response = self.app.put('/employer/one-post', data=json.dumps({'pid': 1, 'title': 'This is a test', 'salary': 3500, 'degree': 'Bachelor', 'label': 'C#', 'tasks': 'test',
             'requirements': 'test', 'inRecruitment': True}), headers={'Authorization': self.loggedEmployerToken},
                                 content_type='application/json')
        resp_json = response.data
        resp_dict = json.loads(resp_json)
        self.assertIn('status', resp_dict)
        status = resp_dict['status']
        self.assertEqual(status, 200)
        self.assertIn('msg', resp_dict)
        msg = resp_dict['msg']
        self.assertEqual(msg, 'Post updated successfully!')

    def test_delete_post(self):
        with app.app_context():
            post = Post.query.filter_by(title='unittest').first()
            response = self.app.delete('/employer/posts', data=json.dumps({'pid': post.pid}),
                                       headers={'Authorization': self.loggedEmployerToken}, content_type='application/json')
            if not response:
                resp_json = response.data
                resp_dict = json.loads(resp_json)
                self.assertIn('status', resp_dict)
                status = resp_dict['status']
                self.assertEqual(status, 200)
                self.assertIn('msg', resp_dict)
                msg = resp_dict['msg']
                self.assertEqual(msg, 'Post deleted successfully!')

    def tearDown(self) -> None:
        with app.app_context():
            self.app.get('/logout/employer', headers={'Authorization': self.loggedEmployerToken}, content_type='application/json')


if __name__ == '__main__':
    unittest.main()

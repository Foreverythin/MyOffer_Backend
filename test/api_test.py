import unittest
import json
import forms

from app import app


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
            print(response.data)
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


if __name__ == '__main__':
    unittest.main()

"""
This file includes the database tests.

All 9 functions are used to test the database, and pass the tests.
"""
import datetime
import unittest
from db_database import app, db, Employee, Employer, Post, Captcha, PostEmployee
import time


class TestUserTable(unittest.TestCase):

    def setUp(self):
        # testing = True
        app.config['TESTING'] = True

        self.app = app

        db.create_all()
        # add data to the database before all tests
        employee = Employee(email='pangyuli92@gmail.com', password='lpy..2002', logged=True)
        db.session.add(employee)
        employer = Employer(email='mn20xx@leeds.ac.uk', password='lpy..2002', logged=True)
        db.session.add(employer)
        db.session.commit()

    def test_append_data(self):
        # employee, add a new employee
        employee = Employee(email='mn20pl@leeds.ac.uk', password='lpy..2002', logged=True)
        db.session.add(employee)
        db.session.commit()
        employee_info = Employee.query.filter_by(email='mn20pl@leeds.ac.uk').first()
        self.assertIsNotNone(employee_info)
        self.assertEqual(employee_info.email, 'mn20pl@leeds.ac.uk')
        self.assertEqual(employee_info.password, 'lpy..2002')
        self.assertEqual(employee_info.logged, True)
        self.assertEqual(employee_info.name, 'Your Name')
        self.assertEqual(employee_info.tel, 'Your Tel')
        self.assertEqual(employee_info.major, 'Your Major')
        self.assertEqual(employee_info.degree, 'Your Degree')

        # employer, add a new employer
        employer = Employer(email='mn20xy@leeds.ac.uk', password='lpy..2002', logged=True)
        db.session.add(employer)
        db.session.commit()
        employer_info = Employer.query.filter_by(email='mn20xy@leeds.ac.uk').first()
        self.assertIsNotNone(employer_info)
        self.assertEqual(employer_info.email, 'mn20xy@leeds.ac.uk')
        self.assertEqual(employer_info.password, 'lpy..2002')
        self.assertEqual(employer_info.logged, True)

        # sleep 1 second to wait for the database operation
        time.sleep(1)

    def test_edit_data(self):
        # employee, edit the data of an employee
        employee_info = Employee.query.filter_by(email='pangyuli92@gmail.com').first()
        employee_info.name = 'Yuli'
        employee_info.tel = '12345678900'
        employee_info.major = 'Computer Science'
        db.session.commit()
        employee_info = Employee.query.filter_by(email='pangyuli92@gmail.com').first()
        self.assertEqual(employee_info.name, 'Yuli')
        self.assertEqual(employee_info.tel, '12345678900')
        self.assertEqual(employee_info.major, 'Computer Science')
        # employer, edit the data of an employer
        employer_info = Employer.query.filter_by(email='mn20xx@leeds.ac.uk').first()
        employer_info.name = 'TIMI'
        employer_info.CEO = 'Yuli'
        db.session.commit()
        employer_info = Employer.query.filter_by(email='mn20xx@leeds.ac.uk').first()
        self.assertEqual(employer_info.name, 'TIMI')
        self.assertEqual(employer_info.CEO, 'Yuli')

    def test_delete_data(self):
        # employee, delete an employee
        employee_info = Employee.query.filter_by(email='pangyuli92@gmail.com').first()
        db.session.delete(employee_info)
        db.session.commit()
        employee_info = Employee.query.filter_by(email='pangyuli92@gmail.com').first()
        self.assertIsNone(employee_info)

        # employer, delete an employer
        employer_info = Employer.query.filter_by(email='mn20xx@leeds.ac.uk').first()
        db.session.delete(employer_info)
        db.session.commit()
        employer_info = Employer.query.filter_by(email='mn20xx@leeds.ac.uk').first()
        self.assertIsNone(employer_info)

        # sleep 1 second to wait for the database operation
        time.sleep(1)

    def tearDown(self):
        # delete all data in the database after all tests
        db.session.remove()
        db.drop_all()


class TestPostTable(unittest.TestCase):

    def setUp(self):
        # testing = True
        app.config['TESTING'] = True

        self.app = app

        db.create_all()
        # add data to the database before all tests
        post = Post(title='unittest', salary=5000, degree='Doctor', label='C#', tasks='The post is for unittest', requirements='requirements', inRecruitment=True, employerId=1)
        db.session.add(post)
        db.session.commit()

    def test_append_data(self):
        # post, add a new post
        post = Post(title='unittest2', salary=6000, degree='Doctor', label='C#', tasks='The post2 is for unittest', requirements='requirements', inRecruitment=True, employerId=1)
        db.session.add(post)
        db.session.commit()
        post_info = Post.query.filter_by(title='unittest2').first()
        self.assertIsNotNone(post_info)
        self.assertEqual(post_info.title, 'unittest2')
        self.assertEqual(post_info.salary, 6000)
        self.assertEqual(post_info.degree, 'Doctor')
        self.assertEqual(post_info.label, 'C#')
        self.assertEqual(post_info.tasks, 'The post2 is for unittest')
        self.assertEqual(post_info.requirements, 'requirements')
        self.assertEqual(post_info.inRecruitment, True)
        self.assertEqual(post_info.employerId, 1)

        # sleep 1 second to wait for the database operation
        time.sleep(1)

    def test_edit_data(self):
        # post, edit the data of a post
        post_info = Post.query.filter_by(title='unittest').first()
        post_info.title = 'unittest2'
        post_info.salary = 6000
        post_info.degree = 'Master'
        post_info.label = 'C#'
        post_info.tasks = 'The post2 is for unittest'
        post_info.requirements = 'requirements'
        post_info.inRecruitment = False
        db.session.commit()
        post_info = Post.query.filter_by(title='unittest2').first()
        self.assertEqual(post_info.title, 'unittest2')
        self.assertEqual(post_info.salary, 6000)
        self.assertEqual(post_info.degree, 'Master')
        self.assertEqual(post_info.label, 'C#')
        self.assertEqual(post_info.tasks, 'The post2 is for unittest')
        self.assertEqual(post_info.requirements, 'requirements')
        self.assertEqual(post_info.inRecruitment, False)

    def test_delete_data(self):
        # post, delete a post
        post_info = Post.query.filter_by(title='unittest').first()
        db.session.delete(post_info)
        db.session.commit()
        post_info = Post.query.filter_by(title='unittest').first()
        self.assertIsNone(post_info)

        # sleep 1 second to wait for the database operation
        time.sleep(1)

    def tearDown(self) -> None:
        # delete all data in the database after all tests
        db.session.remove()
        db.drop_all()


class TestCaptchaTable(unittest.TestCase):

    def setUp(self):
        # testing = True
        app.config['TESTING'] = True

        self.app = app

        db.create_all()
        # add data to the database before all tests
        captcha = Captcha(captchaId='1', email='mn20xx@leeds.ac.uk', captcha='1234', createdTime=datetime.datetime.now())
        db.session.add(captcha)
        db.session.commit()

    def test_append_data(self):
        # captcha, add a new captcha
        captcha = Captcha(captchaId='2', email='mn20yy@leeds.ac.uk', captcha='1234', createdTime=datetime.datetime.now())
        db.session.add(captcha)
        db.session.commit()
        captcha_info = Captcha.query.filter_by(captchaId='2').first()
        self.assertIsNotNone(captcha_info)
        self.assertEqual(captcha_info.captchaId, 2)
        self.assertEqual(captcha_info.email, 'mn20yy@leeds.ac.uk')
        self.assertEqual(captcha_info.captcha, '1234')

    def tearDown(self) -> None:
        # delete all data in the database after all tests
        db.session.remove()
        db.drop_all()


class TestPostEmployeeTable(unittest.TestCase):

    def setUp(self):
        # testing = True
        app.config['TESTING'] = True

        self.app = app

        db.create_all()
        # add data to the database before all tests
        post_employee = PostEmployee(pid=1, uid=1)
        db.session.add(post_employee)
        db.session.commit()

    def test_append_data(self):
        # post_employee, add a new post_employee
        post_employee = PostEmployee(pid=2, uid=2)
        db.session.add(post_employee)
        db.session.commit()
        post_employee_info = PostEmployee.query.filter_by(pid=2).first()
        self.assertIsNotNone(post_employee_info)
        self.assertEqual(post_employee_info.pid, 2)
        self.assertEqual(post_employee_info.uid, 2)

    def tearDown(self) -> None:
        # delete all data in the database after all tests
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()

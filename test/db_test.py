import unittest
from db_database import app, db, Employee
import time


class TestLogin(unittest.TestCase):

    def setUp(self):
        # testing = True
        app.config['TESTING'] = True

        self.app = app

        db.create_all()

    def tearDown(self):
        # delete all data in the database after all tests
        db.session.remove()
        db.drop_all()

    def test_append_data(self):
        employee = Employee(email='mn20pl@leeds.ac.uk', password='lpy..2002', logged=True)
        db.session.add(employee)
        db.session.commit()
        employee_info = Employee.query.filter_by(email='mn20pl@leeds.ac.uk').first()
        print(employee_info.name)
        self.assertIsNotNone(employee_info)

        # sleep 2 second to wait for the database operation
        time.sleep(2)


if __name__ == '__main__':
    unittest.main()

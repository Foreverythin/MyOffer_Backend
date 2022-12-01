"""
This file includes some objects and methods which will be used in other files many times.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

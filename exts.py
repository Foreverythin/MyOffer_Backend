"""
This file includes some objects and methods which will be used in other files many times.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import logging
from logging.handlers import RotatingFileHandler

db = SQLAlchemy()
mail = Mail()

logger = logging.getLogger('MyOffer')
logger.setLevel(logging.INFO)

# set backupCount=1000 to disable the backup
handler = RotatingFileHandler('MyOffer.log', backupCount=1000)
formatter = logging.Formatter(
    '[%(asctime)s] - [%(levelname)s] - [%(name)s] - [module: %(module)s:%(lineno)d] : %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

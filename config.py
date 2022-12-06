"""
The file containing all configuration needed in tha flask application, including the database, mail.

All the configuration will be imported by the flask application.
"""

# sqlite config
SQLALCHEMY_DATABASE_URI = 'sqlite:///./database/MyOffer.sqlite3'

# Prohibit data modification tracking
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Secret key
SECRET_KEY = 'AVerySimpleKey'

# mail config
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = True
MAIL_USERNAME = "1510397456@qq.com"
MAIL_PASSWORD = "vqcwrrixwonwfhgi"
MAIL_DEFAULT_SENDER = "1510397456@qq.com"

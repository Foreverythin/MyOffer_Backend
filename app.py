from flask import Flask
from flask_migrate import Migrate
import config
from exts import db, mail
from models import Employee
from flask_cors import CORS

from blueprints import employee_bp, employer_bp, common_bp

app = Flask(__name__)

app.config.from_object(config)

# allow cross-origin resource sharing
CORS(app, origins='*', supports_credentials=True)

# register the database
db.init_app(app)

# register the blueprints
app.register_blueprint(employee_bp)
app.register_blueprint(employer_bp)
app.register_blueprint(common_bp)

# register the mail
mail.init_app(app)

# register the migration
migrate = Migrate(app, db, render_as_batch=True, compare_type=True, compare_server_default=True, compare_default=True)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!!!'


if __name__ == '__main__':
    app.run()


# status code explanation
# 200: success
# 400: account does not exist
# 401: invalid email or password
# 402: invalid form
# 403: errors when updating the database
# 404: errors when validating the form
# 405: account has already existed
# 406: invalid captcha
# 407: invalid url
# 408: no file uploaded
# 409: JoseError
# 410: the user has not logged in

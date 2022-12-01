from flask import Flask
from flask_migrate import Migrate
import config
from exts import db, mail
from models import Employee

app = Flask(__name__)

app.config.from_object(config)

# register the database
db.init_app(app)

# register the mail
mail.init_app(app)

# register the migrate
migrate = Migrate(app, db, compare_type=True, compare_server_default=True)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!!!'


if __name__ == '__main__':
    app.run()

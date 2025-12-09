from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_simple_captcha import CAPTCHA
app = Flask(__name__)


CONFIG = {
    'SECRET_CAPTCHA_KEY': 'LONG_KEY',
    'CAPTCHA_LENGTH': 6,
    'CAPTCHA_DIGITS': False,
    'EXPIRE_SECONDS': 600,
}
SIMPLE_CAPTCHA = CAPTCHA(config=CONFIG)
app = SIMPLE_CAPTCHA.init_app(app)


# Korrektur
#app.jinja_env.autoescape = False

#app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://shopuser:Heute000@localhost:3333/shopdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Flag{YOU_FOUND_AN_POSSIBLE_KEY}'

db = SQLAlchemy(app)

from pinboard import routes
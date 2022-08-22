from random import randint
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import secrets
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app=app)

app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECURITY_PASSWORD_SALT'] = randint(1, 10)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'Erfan'
app.config['MAIL_PASSWORD'] = '261384'


mail = Mail(app=app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.SignIn'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please Sign In To Access This Page'


def Create_Routes(app):

    from main.Base.routes import base
    from main.Route.BankAccount.routes import accounts
    from main.Route.BankCard.routes import cards
    from main.Route.BankTransaction.routes import transactions
    from main.Route.Products.routes import products
    from main.Route.Users.routes import users
    from main.Route.BankStaticTransaction.routes import static

    app.register_blueprint(base)
    app.register_blueprint(accounts)
    app.register_blueprint(cards)
    app.register_blueprint(transactions)
    app.register_blueprint(products)
    app.register_blueprint(users)
    app.register_blueprint(static)


Create_Routes(app)

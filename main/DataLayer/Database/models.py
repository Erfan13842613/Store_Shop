from flask_login import UserMixin
from main import db, login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    bio = db.Column(db.String(255), nullable=True, default="No Bio Yet !")
    role = db.Column(db.String(255), nullable=False, default="USER")
    phone = db.Column(
        db.String(255), default="You Don't have Any Phone Number Yet !")
    user_is_active = db.Column(db.Integer, nullable=False, default=0)
    secret_code = db.Column(db.Integer, nullable=False)
    # Realation One To Many To UserProduct #ID : 4050
    cilent_product = db.relationship(
        'CilentProduct', backref='user', lazy=True)
    # Realation One To Many To Card #ID : 4048
    cards = db.relationship('Card', backref='user', lazy=True)
    # Realation One To Many To Bank Account #ID : 4049
    bank_accounts = db.relationship('Bank', backref='user', lazy=True)
    # Realation One To Many To Product #ID : 4000
    products = db.relationship('Product', backref='product_owner', lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.phone}','{self.email}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_gender = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    product_price = db.Column(db.Integer, nullable=False)
    product_summary = db.Column(db.String(800), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)  # ID : 4000

    def __repr__(self) -> str:
        return f"Product('{self.product_name}','{self.product_gender}')"


class CilentProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    product_gender = db.Column(db.String(255), nullable=False)
    submited_date = db.Column(db.DateTime, default=datetime.utcnow)
    product_price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), nullable=False)  # ID : 4000

    def __repr__(self) -> str:
        return f"CilentProduct('{self.product_name}')"


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Realation One To Many To BankCard #ID : 4039
    bank_cards = db.relationship('Card', backref='bank_accounts', lazy=True)
    # Realation One To Many To BankTransaction #ID : 5000
    bank_transactions = db.relationship(
        'Transaction', backref='bank', lazy=True)
    # Realation One To Many To StaticTransaction #ID : 4041
    bank_static_transactions = db.relationship(
        'StaticTransaction', backref='bank', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id"), nullable=False)  # ID : 4049


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255), nullable=False)
    card_number = db.Column(db.String(255), nullable=False)
    card_cvv2 = db.Column(db.String(255), nullable=False)
    card_expire_time = db.Column(db.DateTime, nullable=False)
    card_password = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Realation One To Many To BankTransaction #ID : 5001
    bank_transactions = db.relationship(
        'Transaction', backref='card', lazy=True)
    bank_account = db.Column(db.Integer, db.ForeignKey(
        'bank.id'), nullable=False)  # ID : 4039
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remained_money = db.Column(db.Integer, nullable=False)
    changed_money = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(800), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    bank_accounts = db.Column(db.Integer, db.ForeignKey(
        'bank.id'), nullable=False)  # ID : 5000
    bank_cards = db.Column(db.Integer, db.ForeignKey(
        'card.id'), nullable=False)  # ID : 5001


class StaticTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    previous_balance = db.Column(db.Integer, nullable=False)
    remained_money = db.Column(db.Integer, nullable=False)
    changed_money = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(800), nullable=False)
    started_date = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    bank_accounts = db.Column(db.Integer, db.ForeignKey(
        'bank.id'), nullable=False)  # ID : 4041


class StaticSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)

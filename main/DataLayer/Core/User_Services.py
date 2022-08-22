from main.DataLayer.Database.models import Bank, Card, Product, User
from main import db


class User_Service:

    @staticmethod
    def Get_User_By_Email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def Get_User_By_Username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def Get_BankAccount_By_User(current_user):
        return Bank.query.filter_by(user=current_user).first()

    @staticmethod
    def Get_BankCard_By_BankAccount(current_bank):
        return Card.query.filter_by(bank_accounts=current_bank).first()

    @staticmethod
    def Get_BankCards_By_Current_User(current_user):
        return Card.query.filter_by(user=current_user).all()

    @staticmethod
    def Get_All_Products_By_User(current_user):
        return Product.query.filter_by(product_owner=current_user).all()

    @staticmethod
    def Get_User_By_Phone(phone):
        return User.query.filter_by(phone=phone).first()

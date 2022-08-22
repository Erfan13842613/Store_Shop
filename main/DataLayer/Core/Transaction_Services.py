
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import Transaction


class Transaction_Service:
    
    @staticmethod
    def Get_All_Transactions_By_User(current_user):
        user_service =User_Service()
        bank_account=user_service.Get_BankAccount_By_User(current_user)
        return Transaction.query.filter_by(bank=bank_account).all()
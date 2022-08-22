from main.DataLayer.Database.models import Bank


class Bank_Service:
    
    @staticmethod
    def Get_Bank_By_Current_User(current_user):
        return Bank.query.filter_by(user=current_user).first()
    
    @staticmethod
    def Get_All_Bank_Accounts_By_User(current_user):
        return Bank.query.filter_by(user=current_user).all()
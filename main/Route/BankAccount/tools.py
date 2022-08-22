from flask_login import current_user
from main.Core.Db_Core import Public_Service
from main.DataLayer.Database.models import Bank
from main.Route.BankCard.tools import Card_Tools


class Bank_Tools:
    
    global Db_Sec, D_Service, P_Service
    
    @staticmethod
    def Build_Bank_Account(form):
       P_Service=Public_Service(Bank)
       bank = Bank(fullname=form.fullname.data,password=form.password.data,user=current_user)
       Card_Tools.Build_New_Card(bank)
       P_Service.Add_To(bank)
       return True
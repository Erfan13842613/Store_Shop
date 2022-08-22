from main.DataLayer.Database.models import Transaction
from main.Core.Db_Core import Public_Service

class Transaction_Tools:
    
    global P_Service
    
    @staticmethod
    def Do_Transaction(current_bank_account,purchase,bank_card):
        P_Service=Public_Service(Transaction)
        transaction=Transaction(remained_money=int(current_bank_account.balance),
                                changed_money=int(purchase),
                                reason='None Implemented',
                                card=bank_card,
                                bank=current_bank_account)
        P_Service.Add_To(transaction)
        return transaction
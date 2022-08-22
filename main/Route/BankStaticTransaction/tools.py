from ...Core.Db_Core import Public_Service
from main.DataLayer.Database.models import StaticTransaction


class Static_Transaction_Tools:

    global Pu_Service

    @staticmethod
    def Do_Create_Static_Transaction(form, current_bank):
        Pu_Service = Public_Service(StaticTransaction)
        static = StaticTransaction(remained_money=current_bank.balance - form.changed_money.data,
                                   previous_balance=current_bank.balance,
                                   changed_money=form.changed_money.data,
                                   reason=form.reason.data,
                                   started_date=form.started_date.data,
                                   bank=current_bank)
        current_bank.balance = current_bank.balance - form.changed_money.data
        Pu_Service.Save_Changes()
        Pu_Service.Add_To(static)
        return True

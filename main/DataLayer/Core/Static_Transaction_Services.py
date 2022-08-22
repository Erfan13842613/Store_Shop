from main.DataLayer.Database.models import StaticTransaction


class Static_Transaction_Service:
    @staticmethod
    def Get_All_Static_Transaction_By_Bank(bank_account):
        return StaticTransaction.query.filter_by(bank=bank_account).all()

    @staticmethod
    def Get_Paginated_Transactions_By_Bank(page, bank_account):
        return StaticTransaction.query.filter_by(bank=bank_account).paginate(page=page, per_page=5)

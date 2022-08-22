from main import db
from main.DataLayer.Database.models import CilentProduct


class Cilent_Service:

    @staticmethod
    def Get_All_Cilent_Products_By_User(current_user):
        return db.session.query(CilentProduct).filter_by(user=current_user).all()

    @staticmethod
    def Get_All_Same_Cilent_Products_By_User(name,gender):
        return db.session.query(CilentProduct).filter(
            CilentProduct.product_name == name,
            CilentProduct.product_gender == gender
        )\
            .order_by(CilentProduct.product_name.desc())\
            .all()

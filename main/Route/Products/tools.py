from main.Core.Db_Core import Public_Service
from main.DataLayer.Database.models import CilentProduct, Product
from flask_login import current_user


class Product_Tools:
    
    global Db_Sec, D_Service, P_Service
    
    @staticmethod
    def Sign_New_purchase(selected_product,user):
        P_Service = Public_Service(CilentProduct)
        purchase = CilentProduct(product_name=selected_product.product_name,
                                 product_gender=selected_product.product_gender,
                                 product_price=selected_product.product_price,
                                 user=user)
        P_Service.Add_To(purchase)
        return True

    @staticmethod
    def Sign_New_Product(form):
        P_Service=Public_Service(Product)
        product=Product(product_name=form.product_name.data,
                        product_gender=form.product_gender.data,
                        product_price=form.product_price.data,
                        product_summary=form.product_summary.data,
                        product_owner=current_user)
        P_Service.Add_To(product)
        return True
        
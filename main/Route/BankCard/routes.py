from flask import Blueprint, flash, redirect, abort, render_template, request, url_for
from flask_login import current_user, login_required
from main.Core.Db_Core import Public_Service
from main.DataLayer.Core.Bank_Services import Bank_Service
from main.DataLayer.Core.Cilent_Services import Cilent_Service
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import CilentProduct, Product, User
from main.Route.BankCard.forms import Card_Purchase
from main.Route.BankCard.tools import Card_Tools
from main.Route.Products.tools import Product_Tools

cards = Blueprint('cards', __name__)
cilent_service = Cilent_Service()
Db_User = Public_Service(User)
Db_Cilent_Product = Public_Service(CilentProduct)
bank_tools = Card_Tools()
user_service = User_Service()
bank_service = Bank_Service()

@staticmethod
def validate_userbank(current_user):
    user_bank_account=user_service.Get_BankAccount_By_User(current_user)
    if user_bank_account is None:
        flash('You Have No Bank Account , Please Make A New One','danger')
        return True
    return False

@cards.route('/product/purchase', methods=['GET', 'POST'])
@cards.route('/home/product/purchase', methods=['GET', 'POST'])
@login_required
def Purchase():
    
    if validate_userbank(current_user):
        return redirect(url_for('base.HomePage'))
    
    products = cilent_service.Get_All_Cilent_Products_By_User(current_user)
    total_price = 0
    for i in products:
        total_price = total_price + i.product_price
    
    form = Card_Purchase()
    if form.validate_on_submit():
        user_bank = bank_service.Get_Bank_By_Current_User(current_user)
        if bank_tools.Is_Ok_Balance_To_Purchased(user_bank, total_price):
            Db_Cilent_Product.Delete_All(
                cilent_service.Get_All_Cilent_Products_By_User(current_user))
            flash('Your purchase was successful.', 'success')
            return redirect(url_for('cards.Payment_Complete', user_id=user_bank.user.id))
        else:
            flash('Your purchase was unsuccessful. Un Expected Balance ! ', 'danger')
    return render_template('CardTemplate/Card_Purchase.html', form=form)


@cards.route('/products/payment_complete/<int:user_id>')
@cards.route('/home/products/payment_complete/<int:user_id>')
@login_required
def Payment_Complete(user_id):

    user = Db_User.Get_By_Id_Or_404(user_id)

    if validate_userbank(user):
        return redirect(url_for('base.HomePage'))
    
    if user != current_user:
        abort(403)

    user_bank = bank_service.Get_Bank_By_Current_User(user)

    return render_template('CardTemplate/Payment_Complete.html', user=user, user_bank=user_bank)


@cards.route('/remove/preoduct/<int:product_id>')
@cards.route('/home/remove/preoduct/<int:product_id>')
@login_required
def Delete_Cilent_Product(product_id):
    
    product = Db_Cilent_Product.Get_By_Id_Or_404(product_id)
    if product.user != current_user:
        abort(403)
    Db_Cilent_Product.Del_To(product)
    flash('Deleted From Your Directory', 'success')
    return redirect(url_for('base.Cart'))

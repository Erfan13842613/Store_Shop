from flask import Blueprint
from flask import render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required
from main.Base.forms import Search_For_User_Form
import redis

from main.Core.Db_Core import Public_Service
from main.DataLayer.Core.Cilent_Services import Cilent_Service
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import Product, StaticSite, User

base = Blueprint('base', __name__)
Db_Pu_Product = Public_Service(Product)
Db_Pu_User = Public_Service(User)
user_service = User_Service()
Site_Pu_Service = Public_Service(StaticSite)
cilent_service = Cilent_Service()


@base.route('/')
@base.route('/home')
def HomePage():
    products = Db_Pu_Product.Get_All()
    return render_template('BaseTemplate/Home.html', products=products)


@base.route('/user/cart/', methods=['GET', 'POST'])
@base.route('/home/user/cart', methods=['GET', 'POST'])
@login_required
def Cart():
    user_bank_account = user_service.Get_BankAccount_By_User(current_user)
    if user_bank_account is None:
        flash('You Have No Bank Account , Please Make A New One', 'danger')
        return redirect(url_for('base.HomePage'))

    products = cilent_service.Get_All_Cilent_Products_By_User(current_user)

    product_lenght = len(products)
    total_price = 0
    for i in products:
        total_price = total_price + i.product_price

    return render_template('BaseTemplate/Cart.html', products=products, product_lenght=product_lenght, total_price=int(total_price))


@base.route('/about_us')
@base.route('/home/about_us')
def About_Us():
    r = redis.Redis()
    message = r.get('TEXT')
    flash('{} {}'.format(r.get('SEND_SMS'), r.get('USER')))
    if message is None:
        text = Site_Pu_Service.Get_By_Id(0)
        r.set('TEXT', text.text)
        print('Cathced From Database And Setted For Redis')
    else:
        print('Catched From Redis')
    return render_template('BaseTemplate/About_Us.html', message=message)

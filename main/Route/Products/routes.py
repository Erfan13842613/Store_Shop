from flask import Blueprint, flash, redirect, abort, render_template, request, url_for
from flask_login import current_user, login_required
from main.Core.Db_Core import Public_Service
from main.DataLayer.Core.Cilent_Services import Cilent_Service
from main.DataLayer.Database.models import CilentProduct, Product
from main.Route.Products.forms import Build_New_Product_Form
from main.Route.Products.tools import Product_Tools


products = Blueprint('products', __name__)
Db_Product = Public_Service(Product)
product_tools = Product_Tools()
cilent_service = Cilent_Service()


@products.route('/user/new_purchase/<int:product_id>', methods=['GET', 'POST'])
@products.route('/home/user/new_purchase/<int:product_id>', methods=['GET', 'POST'])
def Sign_New_Purchase(product_id):

    if not(current_user.is_authenticated):
        flash('You are not authenticated. Please login to purchase', 'warning')
        return redirect(url_for('base.HomePage'))

    current_product = Db_Product.Get_By_Id_Or_404(product_id)

    if product_tools.Sign_New_purchase(current_product,current_user):
        flash('Added Your Cart !', 'success')

    return redirect(url_for('base.HomePage'))


@products.route('/user/create_product', methods=['GET', 'POST'])
@products.route('/user/create_product', methods=['GET', 'POST'])
@login_required
def Sign_Product():

    if current_user.role == "USER":
        abort(403)

    form = Build_New_Product_Form()
    if form.validate_on_submit():
        if product_tools.Sign_New_Product(form):
            flash('Your new product has been created successfully', 'success')
            return redirect(url_for('base.HomePage'))
    return render_template('ProductTemplate/Sign_Product.html', form=form)


@products.route('/user/update_product/<int:product_id>', methods=['GET', 'POST'])
@products.route('/user/update_product/<int:product_id>', methods=['GET', 'POST'])
def Update_Product(product_id):

    if current_user.role == "USER":
        abort(403)

    product = Db_Product.Get_By_Id_Or_404(product_id)

    if product.product_owner != current_user:
        abort(403)

    form = Build_New_Product_Form()
    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.product_gender = form.product_gender.data
        product.product_price = form.product_price.data
        product.product_summary = form.product_summary.data
        Db_Product.Save_Changes()
        flash('Your Product has been Updated Seccessfully.', 'success')
        return redirect(url_for('base.HomePage'))
    elif request.method == 'GET':
        form.product_name.data = product.product_name
        form.product_gender.data = product.product_gender
        form.product_price.data = product.product_price
        form.product_summary.data = product.product_summary
    return render_template('ProductTemplate/Sign_Product.html', form=form)


@products.route('/user/Delete_Product/<int:product_id>', methods=['GET', 'POST'])
@products.route('/home/user/Delete_Product/<int:product_id>', methods=['GET', 'POST'])
def Delete_Product(product_id):

    if current_user.role == "USER":
        abort(403)

    product = Db_Product.Get_By_Id_Or_404(product_id)

    if product.product_owner != current_user:
        abort(403)

    Db_Product.Del_To(product)
    flash("Your Product Has been deleted.", 'success')
    return redirect(url_for('base.HomePage'))

from flask import Blueprint, flash, redirect, render_template, url_for, abort
from flask_login import login_required, current_user

from main.DataLayer.Core.Bank_Services import Bank_Service

from ...DataLayer.Database.models import Bank
from ...Core.Db_Core import Public_Service
from main.DataLayer.Core.User_Services import User_Service

from main.Route.BankAccount.forms import Create_Bank_Account_Form, Increase_BalanceForm
from main.Route.BankAccount.tools import Bank_Tools

accounts = Blueprint('accounts', __name__)
bank_tools = Bank_Tools()
bank_service = Bank_Service()
user_service = User_Service()
Bank_Pu_Service = Public_Service(Bank)


@accounts.route('/create/bank_account', methods=['GET', 'POST'])
@accounts.route('/home/create/bank_account', methods=['GET', 'POST'])
@login_required
def Create_Bank_Account():
    form = Create_Bank_Account_Form()
    if form.validate_on_submit():
        if bank_tools.Build_Bank_Account(form):
            flash('Your Bank Account has been created successfully', 'success')
            return redirect(url_for('base.HomePage'))
        else:
            flash(
                'There was an error creating your Bank Account. Please try again later.', 'danger')
    return render_template('BankTemplate/Create_Bank_Account.html', form=form)


@accounts.route('/bank_account/<int:bank_id>/charge/balance', methods=['GET', 'POST'])
@accounts.route('/home/bank_account/<int:bank_id>/charge/balance', methods=['GET', 'POST'])
@login_required
def Increase_Balance(bank_id):
    bank_account = Bank_Pu_Service.Get_By_Id_Or_404(bank_id)

    if bank_account.user != current_user:
        abort(403)

    form = Increase_BalanceForm()
    if form.validate_on_submit():
        bank_account.balance = bank_account.balance + form.sallary.data
        Bank_Pu_Service.Save_Changes()
        flash('Your Bank Account With This {} Fullname and {} password includes this {}$ balance has been increased.'.format(
            bank_account.fullname, bank_account.password, bank_account.balance), 'success')
        return redirect(url_for('base.HomePage'))
    return render_template('BankTemplate/Increase_Balance.html', form=form, bank_account=bank_account)


@accounts.route('/continue/as', methods=['GET', 'POST'])
@login_required
def Continue_As():
    accounts = bank_service.Get_All_Bank_Accounts_By_User(current_user)
    return render_template('BankTemplate/Continue_As.html', accounts=accounts)

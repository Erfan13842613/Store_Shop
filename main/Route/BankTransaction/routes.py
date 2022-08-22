from flask import Blueprint, flash, redirect, abort, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from main.Core.Db_Core import Public_Service
from main.DataLayer.Core.Transaction_Services import Transaction_Service
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import Card, Transaction, User
from main.Route.BankTransaction.forms import TransactionForm
from main.Route.Users.tools import User_Tools

transactions = Blueprint('transactions', __name__)
Db_Transaction = Public_Service(Transaction)
trans_tools = Transaction_Service()
user_service = User_Service()
user_tools=User_Tools()


def validate_userbank(current_user):
    user_bank_account=user_service.Get_BankAccount_By_User(current_user)
    if user_bank_account is None:
        flash('You Have No Bank Account , Please Make A New One','danger')
        return True
    return False




@transactions.route('/trans_list', methods=['GET', 'POST'])
@transactions.route('/home/trans_list', methods=['GET', 'POST'])
@login_required
def Transaction_List():
    
    if validate_userbank(current_user):
        return redirect(url_for('base.HomePage'))
    
    if user_tools.Is_Account_Active(current_user):
        flash('Your Account Is Not Active','danger')
        return redirect(url_for('base.HomePage'))

    transactions = trans_tools.Get_All_Transactions_By_User(current_user)
    return render_template('TransactionTemplate/Trans_List.html',transactions=transactions)


@transactions.route('/update/transaction/<int:trans_id>', methods=['GET', 'POST'])
@transactions.route('/home/update/transaction/<int:trans_id>', methods=['GET', 'POST'])
@login_required
def Update_Transaction(trans_id):

    if validate_userbank(current_user):
        return redirect(url_for('base.HomePage'))
    
    transaction = Db_Transaction.Get_By_Id_Or_404(trans_id)

    if transaction.card.user != current_user:
        abort(304)
    
    if user_tools.Is_Account_Active(transaction.card.user):
        flash('Your Account Is Not Active','danger')
        return redirect(url_for('base.HomePage'))

    form = TransactionForm()
    if form.validate_on_submit():
        transaction.remained_money = form.remained_money.data
        transaction.changed_money = form.changed_money.data
        transaction.reason = form.reason.data
        Db_Transaction.Save_Changes()
        flash('Your transaction has been saved successfully', 'success')
        return redirect(url_for('transactions.Transaction_List'))
    elif request.method == 'GET':
        form.remained_money.data = transaction.remained_money
        form.changed_money.data = transaction.changed_money
        form.reason.data = transaction.reason
    return render_template('TransactionTemplate/Transaction.html',form=form)


@transactions.route('/Delete/transaction/<int:trans_id>', methods=['GET', 'POST'])
@transactions.route('/home/Delete/transaction/<int:trans_id>', methods=['GET', 'POST'])
@login_required
def Delete_Transaction(trans_id):

    if validate_userbank(current_user):
        return redirect(url_for('base.HomePage'))
    
    transaction = Db_Transaction.Get_By_Id_Or_404(trans_id)

    if transaction.card.user != current_user:
        abort(304)

    if user_tools.Is_Account_Active(transaction.card.user):
        flash('Your Account Is Not Active','danger')
        return redirect(url_for('base.HomePage'))    

    Db_Transaction.Del_To(transaction)
    flash('Your transaction has been deleted.', 'success')
    return redirect(url_for('transactions.Transaction_List'))

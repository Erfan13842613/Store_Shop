
from flask import Blueprint, render_template, url_for, request, abort, flash, redirect
from flask_login import current_user, login_required

from main.DataLayer.Core.Static_Transaction_Services import Static_Transaction_Service
from main.Route.BankStaticTransaction.forms import Create_Static_Transaction_Form
from main.Route.BankStaticTransaction.tools import Static_Transaction_Tools
from ...DataLayer.Database.models import Bank, StaticTransaction

from ...Core.Db_Core import Public_Service

static = Blueprint('static', __name__)
Bank_Pu_Service = Public_Service(Bank)
static_pu_service = Public_Service(StaticTransaction)
static_service = Static_Transaction_Service()
static_tools = Static_Transaction_Tools()


@static.route('/user/bank/<int:bank_id>/transaction', methods=['GET', 'POST'])
@static.route('/home/user/bank/<int:bank_id>/transaction', methods=['GET', 'POST'])
@login_required
def Static_Transaction(bank_id):
    page = request.args.get('page', 1, type=int)
    bank_account = Bank_Pu_Service.Get_By_Id_Or_404(bank_id)

    if bank_account.user != current_user:
        abort(403)
    transactions = static_service.Get_Paginated_Transactions_By_Bank(page,
                                                                     bank_account)
    return render_template('StaticTransactionTemplate/Static_Transaction_List.html', transactions=transactions, bank_account=bank_account)


@static.route('/create_trans/<int:bank_id>', methods=['GET', 'POST'])
@static.route('/home/create_trans/<int:bank_id>', methods=['GET', 'POST'])
@login_required
def Create_Trans(bank_id):
    account = Bank_Pu_Service.Get_By_Id_Or_404(bank_id)

    if account.user != current_user:
        abort(403)
    form = Create_Static_Transaction_Form()
    if form.validate_on_submit():
        static_tools.Do_Create_Static_Transaction(form, account)
        flash('transaction Submited ', 'success')
        return redirect(url_for('static.Static_Transaction', bank_id=bank_id))
    return render_template('StaticTransactionTemplate/Create_Static_Transaction.html', form=form)


@static.route('/update/trans/<int:trans_id>', methods=['GET', 'POST'])
@static.route('/home/update/trans/<int:trans_id>', methods=['GET', 'POST'])
@login_required
def Update_Trans(trans_id):
    transaction = static_pu_service.Get_By_Id_Or_404(trans_id)

    if transaction.bank.user != current_user:
        abort(403)
    form = Create_Static_Transaction_Form()
    if form.validate_on_submit():
        transaction.bank.balance = transaction.bank.balance - \
            form.changed_money.data
        transaction.remained_money = transaction.previous_balance - form.changed_money.data
        transaction.changed_money = form.changed_money.data
        transaction.reason = form.reason.data
        transaction.started_date = form.started_date.data
        static_pu_service.Save_Changes()
        flash('transaction Updated Successfully', 'success')
        return redirect(url_for('static.Static_Transaction', bank_id=transaction.bank.id))
    elif request.method == 'GET':
        form.changed_money.data = transaction.changed_money
        form.reason.data = transaction.reason
        form.started_date.data = transaction.started_date
    return render_template('StaticTransactionTemplate/Create_Static_Transaction.html', form=form)


@static.route('/delete/trans/<int:trans_id>', methods=['GET', 'POST'])
@static.route('/home/delete/trans/<int:trans_id>', methods=['GET', 'POST'])
@login_required
def Delete_Trans(trans_id):
    transaction = static_pu_service.Get_By_Id_Or_404(trans_id)

    if transaction.bank.user != current_user:
        abort(403)

    static_pu_service.Del_To(transaction)
    flash('Deleted !', 'success')
    return redirect(url_for('static.Static_Transaction', bank_id=transaction.bank.id))

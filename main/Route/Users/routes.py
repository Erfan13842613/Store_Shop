from flask import Blueprint, flash, redirect, abort, render_template, request, url_for
from flask_login import current_user, login_required, logout_user
from main.Core.Db_Core import Public_Service
from main.Core.Security import Email_Token_Security
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import Card, User
from main.Route.Users.forms import AccountForm, ChangePasswordForm, Confrim_Email_Form, SignInForm, SignUpForm
from main.Route.Users.tools import User_Tools
import redis

users = Blueprint('users', __name__)
user_tools = User_Tools()
user_service = User_Service()
Db = Public_Service(User)
Db_Card = Public_Service(Card)
Sec_Service = Email_Token_Security()


@users.route('/signin', methods=['GET', 'POST'])
@users.route('/home/signin', methods=['GET', 'POST'])
def SignIn():

    if current_user.is_authenticated:
        return redirect(url_for('base.HomePage'))

    form = SignInForm()
    if form.validate_on_submit():
        is_ok = user_tools.Login_User(form)
        if is_ok:
            flash('You Signed in successfully.', 'success')
            return redirect(url_for('base.HomePage'))
        if is_ok is False:
            flash('Your email or your password is incorrect !', 'danger')
    return render_template('UserTemplate/SignIn.html', form=form)


@users.route('/signup', methods=['GET', 'POST'])
@users.route('/home/signup', methods=['GET', 'POST'])
def SignUp():

    if current_user.is_authenticated:
        return redirect(url_for('base.HomePage'))

    form = SignUpForm()
    if form.validate_on_submit():
        user = user_tools.SignUp_User(form=form)
        if user:
            flash('Your Account Was Created Successfully !', 'success')
            return redirect(url_for('users.SignIn'))
        else:
            flash('There Was An Error During Signing Up !', 'danger')
    return render_template('UserTemplate/SignUp.html', form=form)


@users.route('/changepassword', methods=['GET', 'POST'])
@users.route('/home/changepassword', methods=['GET', 'POST'])
@login_required
def ChangePassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if user_tools.Change_UserPassword(form):
            flash('Your Password Was Updated Successfully', 'success')
            return redirect(url_for('base.HomePage'))
        else:
            flash('Your password is not correct !', 'danger')
    return render_template('UserTemplate/ChangePassword.html', form=form)


@users.route('/account', methods=['GET', 'POST'])
@users.route('/home/account', methods=['GET', 'POST'])
@login_required
def Account():
    Cards = user_service.Get_BankCards_By_Current_User(current_user)
    return render_template('UserTemplate/Account.html', Cards=Cards)


@users.route('/account/card/<int:card_id>', methods=['GET', 'POST'])
@users.route('/home/account/card/<int:card_id>', methods=['GET', 'POST'])
@login_required
def Account_Card(card_id):

    card = Db_Card.Get_By_Id_Or_404(card_id)

    if current_user != card.bank_accounts.user:
        abort(403)
    Cards = user_service.Get_BankCards_By_Current_User(current_user)
    # I Did not understand what the fuck is going on here...
    return render_template('UserTemplate/AccountCard.html', card=card, Cards=Cards)
    # Puting This Cards Will Fix All The Errors


@users.route('/change/account', methods=['GET', 'POST'])
@users.route('/home/change/account', methods=['GET', 'POST'])
@login_required
def Change_Account_Info():
    form = AccountForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        current_user.phone = "0{}".format(form.phone.data)
        current_user.bio = form.bio.data
        Db.Save_Changes()
        flash('Your account info has been saved.', 'success')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.bio.data = current_user.bio
    return render_template('UserTemplate/Change_Account_Info.html', form=form)


@users.route('/logout')
@users.route('/home/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('base.HomePage'))


@users.route('/active/email/<int:user_id>', methods=['GET', 'POST'])
@users.route('/home/active/email/<int:user_id>', methods=['GET', 'POST'])
@login_required
def Confrim_Email(user_id):
    # Getting User Or 404
    user = Db.Get_By_Id_Or_404(user_id)

    # Checking For Some DumbAss Works
    if user.user_is_active == 1:
        return redirect(url_for('base.HomePage'))
    # Saving In Redis For Have Only One Message For Send # After 2 Min It Will Be Sended Automaticly
    r = redis.Redis()
    is_sms = r.get('{}_SEND_SMS'.format(user.id))
    is_user = r.get(user.username)
    # Checking For Several Message Sending
    if is_sms != 'YES' and is_user == None and is_user != user.username:
        user_tools.Send_Sms(user)
        r.set(user.username, user.username)
        r.set('{}_SEND_SMS'.format(user.id), 'YES')
    form = Confrim_Email_Form()
    if form.validate_on_submit():
        # Checking Seceret Code For Activition
        if form.confrim_code.data == user.secret_code:
            user.user_is_active = 1
            user.secret_code = Sec_Service.Generate_Random_Secret_Key(
                40000, 60000)
            Db.Save_Changes()
            flash('Your Account Is Acctive Know', 'success')
            # Deleteing Stored Data From Redis
            r.delete('{}_SEND_SMS'.format(user.id))
            r.delete(user.username)
            return redirect(url_for('base.HomePage'))
        else:
            flash('Wronge Verify Code', 'danger')

    return render_template('UserTemplate/Confrim_Email.html', form=form, user=user)


@users.route('/Send/Sms/<int:user_id>')
def Send_SMS(user_id):
    user = Db.Get_By_Id_Or_404(user_id)
    if user.user_is_active == 1:
        return redirect(url_for('base.HomePage'))
    user.secret_code = Sec_Service.Generate_Random_Secret_Key(40000, 60000)
    Db.Save_Changes()
    if user_tools.Send_Sms(user) == False:
        flash('This Is Equal To Zero , Error In Merging The Number')
    flash('You Have 2 Mintues To Enter Your Code OtherWise The Code Will Expire !', 'info')
    return redirect(url_for('users.Confrim_Email', user_id=user_id))

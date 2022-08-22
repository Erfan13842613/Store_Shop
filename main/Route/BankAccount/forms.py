from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.DataLayer.Core.Bank_Services import Bank_Service
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import Bank


class Create_Bank_Account_Form(FlaskForm):

    global bank_tools

    fullname = StringField('Full Name', validators=[
                           DataRequired('This field is required')])
    password = PasswordField('Password', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    confrim_password = PasswordField('Confrim_Password', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght'), EqualTo('password', 'This password doesnt exactly matched with the main password')])
    submit = SubmitField('Submit')

    def validate_fullname(self, fullname):
        bank_tools = Bank_Service()
        fullname = Bank.query.filter_by(fullname=fullname.data).first()
        if fullname:
            raise ValidationError(
                'This Fullname Is Already Exist , Please Opt A New One.')


class Increase_BalanceForm(FlaskForm):
    sallary = IntegerField('Sallary', validators=[
                           DataRequired('This Field Is Required')])
    submit = SubmitField('Increase')

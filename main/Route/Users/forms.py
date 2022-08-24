from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.Core.Db_Core import Security
from main.Core.Security import Security_Validator
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import User

Db_User = User_Service()
Security_Val = Security_Validator()
Securities = Security(User)


class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    email = EmailField('Email', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    phone = IntegerField('Phone Number', validators=[
        DataRequired('This Field Is Required')])
    bio = StringField('Bio', validators=[
                      DataRequired('This Field Is Required')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is already taken!')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already taken!')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    confrim_password = PasswordField('Confrim_Password', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght'), EqualTo('password', 'This password doesnt exactly matched with the main password')])
    role = BooleanField('Sign Up As Seller ?')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken!')

    def validate_email(self, email):
        if Security_Val.Validate_Email(email.data):
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already taken!')
        else:
            raise ValidationError('This email is not valid')


class SignInForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght'), Email('This is not a correct format of email')])
    password = PasswordField('Password', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_email(self, email):
        user = Db_User.Get_User_By_Email(email.data)
        if user is None:
            raise ValidationError('This email doesnt exist!')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    new_password = PasswordField('New Password', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    confrim_new_password = PasswordField('ConfrimPassword', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    submit = SubmitField('Change')

    def validate_new_password(self, new_password):
        if Securities.Check_Password_Matching(current_user, new_password.data):
            raise ValidationError(
                'This Is Your Old Password Please Opt A New One !')


class RequestResetForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght'), Email('This is not a correct format of email')])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There Is No Account With That Email.')


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    confrim_new_password = PasswordField('ConfrimPassword', validators=[DataRequired(
        'This Field Is Required'), Length(1, 255, 'More Than Standard Lenght')])
    submit = SubmitField('Reset Password')


class Confrim_Email_Form(FlaskForm):
    confrim_code = IntegerField('Confrim Code', validators=[
                                DataRequired('This Feild Is Required !')])
    submit = SubmitField('Confrim Email')


class Static_Confrim_Email_Form(FlaskForm):
    phone = IntegerField('Phone Number', validators=[
        DataRequired('This Field Is Required')])
    confrim_code = IntegerField('Confrim Code', validators=[
                                DataRequired('This Feild Is Required !')])
    submit = SubmitField('Confrim Email')

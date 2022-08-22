from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.DataLayer.Core.Bank_Services import Bank_Service
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import Bank


class Create_Static_Transaction_Form(FlaskForm):
    changed_money = IntegerField(
        'Spends', validators=[DataRequired('This Field Is Required')])
    reason = TextAreaField('Reason', validators=[
                           DataRequired('This Field Is Required')])
    started_date = StringField('Started Date', validators=[
                               DataRequired('This Field Is Required')])
    submit = SubmitField('Create')

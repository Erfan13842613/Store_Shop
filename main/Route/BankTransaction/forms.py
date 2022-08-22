from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,TextAreaField,IntegerField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from main.DataLayer.Core.User_Services import User_Service
from main.DataLayer.Database.models import User

class TransactionForm(FlaskForm):
    remained_money=IntegerField('Remained money',validators=[DataRequired('This Feild is required')])
    changed_money=IntegerField('Changed money',validators=[DataRequired('This Feild is required')])
    reason=TextAreaField('Reason',validators=[DataRequired('This Feild is required')])
    submit=SubmitField('Submit')